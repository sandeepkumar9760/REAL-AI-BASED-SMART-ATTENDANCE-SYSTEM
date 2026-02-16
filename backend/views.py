from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Student
import base64, uuid, os, json
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from backend.ai.face_ai import decode_base64_image, recognize_faces
from backend.models import AttendanceSession, Attendance, Student, Subject, ClassRoom
import numpy as np
import cv2
import pickle
import face_recognition
from django.http import JsonResponse
from .models import Student


from .models import (
    Student,
    ClassRoom,
    Subject,
    AttendanceSession,
    Attendance
)
from django.db.models import Count, Q
from django.utils import timezone

from django.shortcuts import render

def analytics_dashboard(request):
    return render(request, "analytics_dashboard.html")

def attendance_analytics(request):

    classroom_id = request.GET.get("classroom_id")
    subject_id = request.GET.get("subject_id")

    attendance_qs = Attendance.objects.select_related(
        "student",
        "attendance_session",
        "attendance_session__classroom",
        "attendance_session__subject"
    )

    # Apply filters
    if classroom_id:
        attendance_qs = attendance_qs.filter(
            attendance_session__classroom_id=classroom_id
        )

    if subject_id:
        attendance_qs = attendance_qs.filter(
            attendance_session__subject_id=subject_id
        )

    total_students = Student.objects.filter(is_active=True).count()
    total_sessions = AttendanceSession.objects.count()

    total_records = attendance_qs.count()
    present_count = attendance_qs.filter(is_present=True).count()
    absent_count = attendance_qs.filter(is_present=False).count()

    overall_rate = (
        (present_count / total_records) * 100
        if total_records > 0 else 0
    )

    # ===== DAILY TREND =====
    last_7_sessions = (
        AttendanceSession.objects
        .order_by('-date')[:7]
    )

    daily_stats = []

    for session in last_7_sessions:
        session_records = attendance_qs.filter(attendance_session=session)

        total = session_records.count()
        present = session_records.filter(is_present=True).count()

        rate = (present / total) * 100 if total > 0 else 0

        daily_stats.append({
            "date": session.date.strftime("%Y-%m-%d"),
            "attendance_rate": round(rate, 2)
        })

    # ===== TOP ABSENT STUDENTS =====
    top_absent = (
        attendance_qs
        .filter(is_present=False)
        .values("student__name")
        .annotate(absent_count=Count("id"))
        .order_by("-absent_count")[:5]
    )

    # ===== RISK DETECTION (Below 60%) =====
    student_stats = (
        attendance_qs
        .values("student__name")
        .annotate(
            total=Count("id"),
            present=Count("id", filter=Q(is_present=True))
        )
    )

    risk_students = []

    for s in student_stats:
        if s["total"] > 0:
            rate = (s["present"] / s["total"]) * 100
            if rate < 60:
                risk_students.append({
                    "name": s["student__name"],
                    "rate": round(rate, 2)
                })

    return JsonResponse({
        "summary": {
            "total_students": total_students,
            "total_sessions": total_sessions,
            "overall_rate": round(overall_rate, 2),
            "present_count": present_count,
            "absent_count": absent_count,
        },
        "daily_stats": daily_stats,
        "top_absent": list(top_absent),
        "risk_students": risk_students
    })
# -------------------------
# LOGIN PAGE
# -------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


# -------------------------
# DASHBOARD PAGE
# -------------------------
@login_required(login_url="login")
def dashboard_view(request):
    today = timezone.now().date()

    total_students = Student.objects.filter(is_active=True).count()
    present_today = Attendance.objects.filter(
        attendance_session__date=today,
        is_present=True
    ).count()
    absent_today = Attendance.objects.filter(
        attendance_session__date=today,
        is_present=False
    ).count()

    context = {
        "total_students": total_students,
        "present_today": present_today,
        "absent_today": absent_today,
    }

    return render(request, "dashboard.html", context)





def get_students(request):
    classroom_id = request.GET.get("classroom_id")

    if not classroom_id:
        return JsonResponse({"students": []})

    students = Student.objects.filter(
        classroom_id=classroom_id,
        is_active=True
    ).values("id", "name", "roll_number")

    return JsonResponse({"students": list(students)})

# -------------------------
# ATTENDANCE PAGE
# -------------------------
@login_required(login_url="login")
def attendance_view(request):
    classrooms = ClassRoom.objects.all()
    subjects = Subject.objects.all()

    if request.method == "POST":
        classroom_id = request.POST.get("classroom")
        subject_id = request.POST.get("subject")
        date = timezone.now().date()

        classroom = get_object_or_404(ClassRoom, id=classroom_id)
        subject = get_object_or_404(Subject, id=subject_id)

        # Create or get attendance session
        session, created = AttendanceSession.objects.get_or_create(
            classroom=classroom,
            subject=subject,
            date=date,
        )

        absentees = []
        students = Student.objects.filter(classroom=classroom, is_active=True)

        for student in students:
            present = request.POST.get(f"present_{student.id}") == "on"

            Attendance.objects.update_or_create(
                attendance_session=session,
                student=student,
                defaults={"is_present": present}
            )

            if not present:
                absentees.append(student.name)

        return render(
            request,
            "attendance_result.html",
            {"absentees": absentees}
        )

    context = {
        "classrooms": classrooms,
        "subjects": subjects,
    }

    return render(request, "attendance.html", context)


# -------------------------
# LOGOUT
# -------------------------
@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return redirect("login")

def decode_base64_image(image_data):
    """
    Decodes base64 image from frontend camera
    """
    format, imgstr = image_data.split(';base64,')
    img_bytes = base64.b64decode(imgstr)

    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def recognize_faces(image, classroom_id):
    """
    Recognizes faces only among students of a specific classroom
    """

    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    if not face_encodings:
        return []

    matched_students = []

    students = Student.objects.filter(
        classroom_id=classroom_id,
        face_encoding__isnull=False
    )

    for face_encoding in face_encodings:
        for student in students:
            stored_encoding = pickle.loads(student.face_encoding)

            matches = face_recognition.compare_faces(
                [stored_encoding],
                face_encoding,
                tolerance=0.5
            )

            if True in matches:
                matched_students.append(student)

    return matched_students


@csrf_exempt
def camera_ai_detect(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    data = json.loads(request.body)
    image_data = data.get("image")
    classroom_id = data.get("classroom_id")
    subject_id = data.get("subject_id")  # <-- we will send this from frontend

    if not image_data or not classroom_id or not subject_id:
        return JsonResponse({"error": "Missing data"}, status=400)

    # Decode image & recognize faces
    image = decode_base64_image(image_data)
    present_students = recognize_faces(image, classroom_id)

    today = timezone.now().date()

    # Get or create session (prevents duplicates)
    attendance_session, created = AttendanceSession.objects.get_or_create(
        classroom_id=classroom_id,
        subject_id=subject_id,
        date=today,
        defaults={"faculty": request.user.faculty if hasattr(request.user, "faculty") else None}
    )

    # All students of this class
    all_students = Student.objects.filter(classroom_id=classroom_id)

    present_ids = {s.id for s in present_students}

    # Save attendance
    for student in all_students:
        Attendance.objects.update_or_create(
            attendance_session=attendance_session,
            student=student,
            defaults={"is_present": student.id in present_ids}
        )

    return JsonResponse({
        "present": [s.name for s in present_students],
        "absent": [
            s.name for s in all_students if s.id not in present_ids
        ],
        "session_created": created
    })


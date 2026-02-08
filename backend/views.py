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

from backend.ai.face_ai import load_known_faces, recognize_faces
from backend.models import ClassRoom



from .models import (
    Student,
    ClassRoom,
    Subject,
    AttendanceSession,
    Attendance
)


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

@csrf_exempt
def camera_ai_detect(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    data = json.loads(request.body)
    image_data = data.get("image")
    classroom_id = data.get("classroom_id")

    classroom = Classroom.objects.get(id=classroom_id)

    # Save classroom image temporarily
    format, imgstr = image_data.split(";base64,")
    image_bytes = base64.b64decode(imgstr)

    temp_dir = os.path.join(settings.MEDIA_ROOT, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    filename = f"classroom_{uuid.uuid4()}.jpg"
    image_path = os.path.join(temp_dir, filename)

    with open(image_path, "wb") as f:
        f.write(image_bytes)

    # AI Recognition
    known_encodings, known_students = load_known_faces(classroom)
    recognized_students = recognize_faces(
        image_path,
        known_encodings,
        known_students
    )

    return JsonResponse({
        "recognized_students": [
            {
                "id": s.id,
                "name": s.name,
                "roll_number": s.roll_number
            }
            for s in recognized_students
        ]
    })

from django.shortcuts import render, redirect
from django.contrib import messages


# -------------------------
# LOGIN PAGE
# -------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Temporary static login (replace later)
        if username == "admin" and password == "admin123":
            request.session["user"] = username
            return redirect("dashboard")

        messages.error(request, "Invalid username or password")

    return render(request, "login.html")


# -------------------------
# DASHBOARD PAGE
# -------------------------
def dashboard_view(request):
    if "user" not in request.session:
        return redirect("login")

    context = {
        "total_students": 60,
        "present_today": 52,
        "absent_today": 8
    }
    return render(request, "dashboard.html", context)


# -------------------------
# ATTENDANCE PAGE
# -------------------------
def attendance_view(request):
    if "user" not in request.session:
        return redirect("login")

    students = [
        {"roll": 1, "name": "Rahul"},
        {"roll": 2, "name": "Aman"},
        {"roll": 3, "name": "Neha"},
        {"roll": 4, "name": "Priya"},
    ]

    if request.method == "POST":
        absentees = []

        for student in students:
            if not request.POST.get(f"present_{student['roll']}"):
                absentees.append(student["name"])

        return render(request, "attendance_result.html", {
            "absentees": absentees
        })

    return render(request, "attendance.html", {"students": students})


# -------------------------
# LOGOUT
# -------------------------
def logout_view(request):
    request.session.flush()
    return redirect("login")

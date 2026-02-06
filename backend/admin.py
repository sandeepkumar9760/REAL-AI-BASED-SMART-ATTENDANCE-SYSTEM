from django.contrib import admin
from .models import (
    Faculty,
    ClassRoom,
    Student,
    Subject,
    AttendanceSession,
    Attendance,
    FaceData
)


# -----------------------------
# FACULTY ADMIN
# -----------------------------
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("username", "name", "department", "is_active", "created_at")
    list_filter = ("department", "is_active")
    search_fields = ("username", "name")
    ordering = ("name",)


# -----------------------------
# CLASSROOM ADMIN
# -----------------------------
@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "year", "created_at")
    list_filter = ("department", "year")
    search_fields = ("name",)
    ordering = ("year", "name")


# -----------------------------
# STUDENT ADMIN
# -----------------------------
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "roll_number",
        "name",
        "classroom",
        "parent_contact",
        "is_active",
        "created_at",
    )
    list_filter = ("classroom", "is_active")
    search_fields = ("roll_number", "name")
    ordering = ("roll_number",)


# -----------------------------
# SUBJECT ADMIN
# -----------------------------
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "classroom", "faculty", "created_at")
    list_filter = ("classroom", "faculty")
    search_fields = ("name",)
    ordering = ("classroom", "name")


# -----------------------------
# ATTENDANCE SESSION ADMIN
# -----------------------------
@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ("classroom", "subject", "faculty", "date", "created_at")
    list_filter = ("classroom", "subject", "date")
    search_fields = ("classroom__name", "subject__name")
    date_hierarchy = "date"
    ordering = ("-date",)


# -----------------------------
# ATTENDANCE RECORD ADMIN
# -----------------------------
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "attendance_session",
        "is_present",
        "marked_at",
    )
    list_filter = ("is_present", "attendance_session__date")
    search_fields = ("student__name",)
    ordering = ("-marked_at",)


# -----------------------------
# FACE DATA ADMIN
# -----------------------------
@admin.register(FaceData)
class FaceDataAdmin(admin.ModelAdmin):
    list_display = ("student", "updated_at")
    search_fields = ("student__name",)

from django.db import models


# -----------------------------
# FACULTY MODEL
# -----------------------------
class Faculty(models.Model):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.department})"


# -----------------------------
# CLASSROOM MODEL
# -----------------------------
class ClassRoom(models.Model):
    name = models.CharField(max_length=20, unique=True)   # e.g. CSE-3A
    department = models.CharField(max_length=50)
    year = models.PositiveIntegerField()  # 1, 2, 3, 4

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# -----------------------------
# STUDENT MODEL
# -----------------------------
class Student(models.Model):
    roll_number = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE,
        related_name="students"
    )
    face_image = models.ImageField(
        upload_to="student_faces/",
        null=True,
        blank=True
    )
    parent_contact = models.CharField(max_length=15)
    face_image = models.ImageField(upload_to='student_faces/', null=True, blank=True)

    face_encoding = models.BinaryField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.roll_number} - {self.name}"


# -----------------------------
# SUBJECT MODEL
# -----------------------------
class Subject(models.Model):
    name = models.CharField(max_length=100)
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE,
        related_name="subjects"
    )
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        related_name="subjects"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("name", "classroom")

    def __str__(self):
        return f"{self.name} - {self.classroom.name}"


# -----------------------------
# ATTENDANCE SESSION (PER CLASS & SUBJECT)
# -----------------------------
class AttendanceSession(models.Model):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("classroom", "subject", "date")

    def __str__(self):
        return f"{self.classroom} | {self.subject} | {self.date}"


# -----------------------------
# ATTENDANCE RECORD (PER STUDENT)
# -----------------------------
class Attendance(models.Model):
    attendance_session = models.ForeignKey(
    AttendanceSession,
    on_delete=models.CASCADE,
    related_name="records",
    null=True,
    blank=True
)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)

    marked_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("attendance_session", "student")

    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student.name} - {status}"


# -----------------------------
# FACE DATA MODEL (AI READY)
# -----------------------------
class FaceData(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="faces/")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.name

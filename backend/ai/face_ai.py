import base64
import cv2
import numpy as np
import face_recognition
from backend.models import Student
from django.conf import settings
import os


def decode_base64_image(data):
    header, encoded = data.split(",", 1)
    img_bytes = base64.b64decode(encoded)
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)
    return cv2.imdecode(img_array, cv2.IMREAD_COLOR)


def get_student_encoding(student):
    """
    Load student's face image and compute encoding
    """
    if not student.face_image:
        return None

    image_path = os.path.join(settings.MEDIA_ROOT, student.face_image.name)
    if not os.path.exists(image_path):
        return None

    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)

    if encodings:
        return encodings[0]
    return None


def recognize_faces(classroom_image, classroom_id):
    rgb_img = cv2.cvtColor(classroom_image, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_img)
    face_encodings = face_recognition.face_encodings(rgb_img, face_locations)

    students = Student.objects.filter(
        classroom_id=classroom_id,
        face_image__isnull=False
    )

    known_encodings = []
    known_students = []

    for student in students:
        encoding = get_student_encoding(student)
        if encoding is not None:
            known_encodings.append(encoding)
            known_students.append(student)

    present_students = set()

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(
            known_encodings, face_encoding, tolerance=0.45
        )

        for i, matched in enumerate(matches):
            if matched:
                present_students.add(known_students[i])

    return present_students

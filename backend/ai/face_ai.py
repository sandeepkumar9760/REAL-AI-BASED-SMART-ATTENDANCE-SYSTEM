import face_recognition
from backend.models import Student


def load_known_faces(classroom):
    known_encodings = []
    known_students = []

    students = Student.objects.filter(classroom=classroom)

    for student in students:
        if not student.face_image:
            continue

        image = face_recognition.load_image_file(student.face_image.path)
        encodings = face_recognition.face_encodings(image)

        if encodings:
            known_encodings.append(encodings[0])
            known_students.append(student)

    return known_encodings, known_students


def recognize_faces(classroom_image_path, known_encodings, known_students):
    image = face_recognition.load_image_file(classroom_image_path)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    recognized_students = set()

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(
            known_encodings,
            face_encoding,
            tolerance=0.5
        )

        if True in matches:
            index = matches.index(True)
            recognized_students.add(known_students[index])

    return recognized_students

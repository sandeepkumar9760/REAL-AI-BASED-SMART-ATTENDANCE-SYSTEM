import face_recognition
import pickle
import cv2
import numpy as np


def generate_face_encoding_from_image(image_path):
    """
    Takes image path and returns serialized face encoding.
    """

    # Load image
    image = face_recognition.load_image_file(image_path)

    # Detect faces and compute encodings
    encodings = face_recognition.face_encodings(image)

    if len(encodings) == 0:
        return None

    # Take first detected face
    encoding = encodings[0]

    # Serialize encoding
    return pickle.dumps(encoding)


def generate_face_encoding_from_uploaded_file(uploaded_file):
    """
    Takes Django uploaded image file and returns serialized encoding.
    """

    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    encodings = face_recognition.face_encodings(rgb_image)

    if len(encodings) == 0:
        return None

    encoding = encodings[0]

    return pickle.dumps(encoding)

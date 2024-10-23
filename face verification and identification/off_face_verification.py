from deepface import DeepFace
import face_recognition
import os
import numpy as np
import cv2

# Function for face matching
def match_faces(image1_path, image2_path):
    backends = [
        'opencv',
        'ssd',
        'dlib',  # DO NOT USE, IS NOT CURRENTLY INSTALLED
        'mtcnn',
        'fastmtcnn',
        'retinaface',
        'mediapipe',
        'yolov8',
        'yunet',
        'centerface',
    ]

    alignment_modes = [True, False]

    # Face verification
    obj = DeepFace.verify(
        img1_path=image1_path,
        img2_path=image2_path,
        detector_backend=backends[0],  # You can change the backend if needed
        align=alignment_modes[0]  # Whether or not to align faces
    )

    # Return only whether the faces matched or not
    return obj["verified"]

def LoadEncodings(dir):
    faces = os.listdir(dir)
    images_known = []
    for x in faces:
        images_known.append(dir + "/" + x)
    known_face_encodings = []
    known_face_names = []
    for x in images_known:
        known_image = face_recognition.load_image_file(x)
        known_face_encoding = face_recognition.face_encodings(known_image, model="large")[0]
        known_face_encodings.append(known_face_encoding)
        known_face_names.append(os.path.basename(x))

    return known_face_encodings, known_face_names

def rec_face(image_path, encodings_path):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image, model="cnn")
    face_encodings = face_recognition.face_encodings(image, face_locations, model="large")
    known_face_encodings, known_face_names = LoadEncodings(encodings_path)
    
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        
        cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(image, os.path.splitext(name)[0], (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imwrite("output.jpg", image)


import cv2
from deepface import DeepFace
import numpy as np
import os

class FaceVerifier:
    def __init__(self, registration_path="face_registration.jpg"):
        self.registration_path = registration_path
        self.registered = False

    def register_face(self, frame):
        cv2.imwrite(self.registration_path, frame)
        self.registered = True
        return True

    def verify_face(self, frame):
        if not self.registered or not os.path.exists(self.registration_path):
            return False, "No face registered."
        try:
            result = DeepFace.verify(frame, self.registration_path, enforce_detection=False)
            verified = result['verified']
            return verified, result
        except Exception as e:
            return False, str(e)

    def detect_multiple_faces(self, frame):
        faces = DeepFace.extract_faces(frame, enforce_detection=False)
        return len(faces)

# Example usage:
# verifier = FaceVerifier()
# verifier.register_face(frame)
# is_verified, result = verifier.verify_face(frame)
# num_faces = verifier.detect_multiple_faces(frame)

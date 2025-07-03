import cv2
import os

def analyze_video(video_path, output_dir="video_frames"):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    frame_count = 0
    faces_detected = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) > 0:
            faces_detected += 1
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imwrite(os.path.join(output_dir, f"frame_{frame_count}.jpg"), frame)
        frame_count += 1
    cap.release()
    return faces_detected

if __name__ == "__main__":
    video_file = os.path.join("video", "output_video.avi")
    print(f"Faces detected in frames: {analyze_video(video_file)}")

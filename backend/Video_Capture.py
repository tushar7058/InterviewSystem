import cv2
import pyaudio
import wave
import threading
import os

# Create folders if they don't exist
os.makedirs("audio", exist_ok=True)
os.makedirs("video", exist_ok=True)

# Audio recording parametersq
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "audio/output_audio.wav"
VIDEO_OUTPUT_FILENAME = "video/output_video.avi"

# Function to record audio
def record_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording Audio...")

    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording audio")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the audio data as WAV file inside audio/ folder
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Function to record video
def record_video():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open webcam")
        return

    # Define the codec and create VideoWriter object to save video inside video/ folder
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(VIDEO_OUTPUT_FILENAME, fourcc, 20.0,
                          (int(cap.get(3)), int(cap.get(4))))

    print("Recording Video... Press 'q' to stop early")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        cv2.imshow('Recording Video', frame)
        out.write(frame)

        # Press q to stop recording before RECORD_SECONDS
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("Finished recording video")

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Run audio and video recording in parallel
    t1 = threading.Thread(target=record_audio)
    t2 = threading.Thread(target=record_video)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

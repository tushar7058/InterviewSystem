import speech_recognition as sr
import os

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio."
    except sr.RequestError as e:
        return f"STT request failed: {e}"

if __name__ == "__main__":
    audio_file = os.path.join("audio", "output_audio.wav")
    print(transcribe_audio(audio_file))
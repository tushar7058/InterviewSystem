import os
import whisper

def transcribe_audio_whisper(audio_path, model_size="base"):
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result["text"]

if __name__ == "__main__":
    audio_file = os.path.join("audio", "output_audio.wav")
    print(transcribe_audio_whisper(audio_file))

from fastapi import APIRouter, UploadFile, File
import os
from stt.stt_service import transcribe_audio
from webrtc.video_analysis import analyze_video
from utils.pdf_report import generate_pdf_report
from utils.nlp_analysis import analyze_text
from db.models import save_result

router = APIRouter()

@router.post("/process-interview/")
def process_interview(audio: UploadFile = File(...), video: UploadFile = File(...)):
    audio_path = os.path.join("audio", audio.filename)
    video_path = os.path.join("video", video.filename)
    with open(audio_path, "wb") as f:
        f.write(audio.file.read())
    with open(video_path, "wb") as f:
        f.write(video.file.read())
    transcript = transcribe_audio(audio_path)
    faces_detected = analyze_video(video_path)
    sentiment = analyze_text(transcript)
    report_path = generate_pdf_report(transcript, faces_detected)
    save_result(transcript, sentiment, faces_detected, report_path)
    return {
        "transcript": transcript,
        "faces_detected": faces_detected,
        "sentiment": sentiment,
        "report": report_path
    }

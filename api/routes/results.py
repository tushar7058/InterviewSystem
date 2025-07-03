from fastapi import APIRouter
from db.models import SessionLocal, InterviewResult

router = APIRouter()

@router.get("/results/")
def get_results():
    session = SessionLocal()
    results = session.query(InterviewResult).all()
    session.close()
    return [
        {
            "id": r.id,
            "transcript": r.transcript,
            "sentiment": r.sentiment,
            "faces_detected": r.faces_detected,
            "report_path": r.report_path
        } for r in results
    ]

from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class InterviewResult(Base):
    __tablename__ = 'interview_results'
    id = Column(Integer, primary_key=True)
    transcript = Column(Text)
    sentiment = Column(String(50))
    faces_detected = Column(Integer)
    report_path = Column(String(255))

engine = create_engine('sqlite:///db/interview_results.db')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def save_result(transcript, sentiment, faces_detected, report_path):
    session = SessionLocal()
    result = InterviewResult(
        transcript=transcript,
        sentiment=str(sentiment),
        faces_detected=faces_detected,
        report_path=report_path
    )
    session.add(result)
    session.commit()
    session.close()

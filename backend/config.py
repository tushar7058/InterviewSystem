import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///db/interview_results.db")
    # Directories
    AUDIO_DIR: str = os.getenv("AUDIO_DIR", "audio/")
    VIDEO_DIR: str = os.getenv("VIDEO_DIR", "video/")
    REPORTS_DIR: str = os.getenv("REPORTS_DIR", "reports/")
    LOGS_DIR: str = os.getenv("LOGS_DIR", "logs/")
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    # Other settings can be added here

settings = Settings()

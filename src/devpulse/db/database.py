import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from devpulse.db.models import ActivitySession, Base

load_dotenv()

USERNAME = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql+psycopg://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/devpulse"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


def save_sessions(session):
    db = SessionLocal()

    try:
        for activity in session:
            db.add(
                ActivitySession(
                    application=activity.application,
                    pid=activity.pid,
                    window_handle=activity.window_handle,
                    window_title=activity.window_title,
                    start_time=activity.start_time,
                    end_time=activity.end_time,
                    duration=activity.duration
                )
            )
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

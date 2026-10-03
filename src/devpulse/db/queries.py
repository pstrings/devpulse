from datetime import datetime

from devpulse.db.database import SessionLocal
from devpulse.db.models import ActivitySession


def get_sessions(start_time: datetime, end_time: datetime):
    db = SessionLocal()

    try:
        return (
            db.query(ActivitySession)
            .filter(
                ActivitySession.start_time < end_time,
                ActivitySession.end_time > start_time,
            )
            .order_by(ActivitySession.start_time)
            .all()
        )
    finally:
        db.close()

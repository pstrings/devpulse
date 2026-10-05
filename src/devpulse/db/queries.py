from datetime import datetime

from sqlalchemy import func

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


def get_duration_by_application(start_time: datetime, end_time: datetime):
    db = SessionLocal()

    try:
        return (
            db.query(
                ActivitySession.application,
                func.sum(ActivitySession.duration).label("total_duration")
            )
            .filter(
                ActivitySession.start_time >= start_time,
                ActivitySession.end_time <= end_time,
            )
            .group_by(ActivitySession.application)
            .order_by(func.sum(ActivitySession.duration).desc())
            .all()
        )
    finally:
        db.close()

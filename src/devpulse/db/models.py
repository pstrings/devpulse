from sqlalchemy import TIMESTAMP, Column, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class ActivitySession(Base):
    __tablename__ = 'activity_sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    application = Column(String, nullable=False)
    pid = Column(Integer, nullable=False)
    window_handle = Column(Integer, nullable=False)
    window_title = Column(String, nullable=False)
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    duration = Column(Float, nullable=False)

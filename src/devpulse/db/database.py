import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from devpulse.db.models import Base

load_dotenv()

USERNAME = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql+psycopg://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/devpulse"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

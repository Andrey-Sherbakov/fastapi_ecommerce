import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASS')}@{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}",
    echo=True
)
session_local = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

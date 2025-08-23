import os
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fiscus.db")
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    from .models import Customer, Invoice  # noqa
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)

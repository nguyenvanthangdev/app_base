from sqlmodel import create_engine, Session
from app.core.config import settings
from contextlib import contextmanager  # Thêm dòng này

engine = create_engine(settings.DATABASE_URL, echo=True)

@contextmanager  # Thêm dòng này
def get_session():
    with Session(engine) as session:
        yield session

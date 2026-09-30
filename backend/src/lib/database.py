from sqlalchemy import create_engine
from .config import DATABASE_URL

from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args={"connect_timeout": 10})

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

class Base(DeclarativeBase):
    pass
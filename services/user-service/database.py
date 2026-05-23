# services/user-service/database.py

import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

logger = logging.getLogger("user-service.db")

# Read from environment — injected by docker-compose or K8s Secret
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://devops:devops123@db:5432/userdb",
)

# pool_pre_ping=True reconnects if the DB dropped the connection
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI dependency that yields a DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables defined by ORM models. Safe to call multiple times."""
    from models import User  # noqa: F401  — import triggers model registration
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialised")
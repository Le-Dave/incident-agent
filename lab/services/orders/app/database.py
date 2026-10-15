import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Set in docker-compose.yml, e.g. postgresql+psycopg://user:password@postgres:5432/orders
DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    """Parent class for all tables."""


def get_db():
    """Gives each request its own database session, closed at the end."""
    with SessionLocal() as db:
        yield db

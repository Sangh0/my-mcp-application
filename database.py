import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DB_PATH = os.path.join(os.path.dirname(__file__), "people.db")
engine = create_engine(f"sqlite:///{DB_PATH}", future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

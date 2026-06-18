import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Railway provee DATABASE_URL automáticamente al conectar PostgreSQL
# En local puedes crear un .env con esta variable o usa SQLite como fallback
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

# SQLAlchemy necesita el prefijo postgresql:// en vez de postgres://
# Railway a veces da postgres:// — esto lo corrige automáticamente
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# connect_args solo aplica a SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

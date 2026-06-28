from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from app.config import settings
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = settings.Database_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    Db = SessionLocal()
    try:
        yield Db
    finally:
        Db.close()

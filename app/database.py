from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from config import settings
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = settings.Database_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    Db = SessionLocal()
    try:
        yield Db
    finally:
        Db.close()
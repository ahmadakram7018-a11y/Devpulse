from fastapi import FastAPI
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DevPulse API", version="1.0.0")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "DevPulse API is running"}

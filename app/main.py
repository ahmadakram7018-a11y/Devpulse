from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routers import posts, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DevPulse API", version="1.0.0")

app.include_router(posts.router)
app.include_router(users.router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "DevPulse API is running"}



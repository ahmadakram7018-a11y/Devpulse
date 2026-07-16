from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routers import posts, users , auth, votes, comment
from app.utils.logger import setup_logger

app = FastAPI(title="DevPulse API", version="1.0.0")
logger = setup_logger(__name__)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)
app.include_router(comment.router)



@app.get("/")
def health_check():
    return {"status": "ok", "message": "Welcome to Devpulse. World Best Developers Collaboration Platform"}


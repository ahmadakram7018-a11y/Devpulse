from fastapi import FastAPI
from app.database import engine, Base
from app import models

Base.metadata.create_all(bind=engine) # every model created use the Base class inside, so when we import all these models inside main.py, this code create these models by using create_all method of the Base class and bind it to the engine we created in database.py
# bind= engine, because engine establish connection to DB, so it knows which DB(like Postresql,etc) to establish connection to and create the tables(models) in that DB.without bind=engine, it will not know which DB to create the tables(models) in.

app = FastAPI(title="DevPulse API", version="1.0.0")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "DevPulse API is running"}


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import database
from app.database.models import *
from app.database.repositories import *
from app.database.schemes import *

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.post("/")
def m1():
    pass

@app.get("/")
def m2():
    pass

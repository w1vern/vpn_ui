from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import database


app = FastAPI()

@app.post("/")
def m1():
    pass

@app.get("/")
def m2():
    pass

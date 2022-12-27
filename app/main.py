# Modules import
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel

from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from sqlalchemy.orm import Session
from . import models,schemas, utils
from . database import engine,  get_db

from .routers import posts, users


# this line crate the table whe we run the code
models.Base.metadata.create_all(bind=engine)


# Fastapi instantiation
app = FastAPI()


# Handel the database connection hard coded
while True:
    try:
        conn = psycopg2.connect(host="hostName",database="dbName", user="userName", password="password", cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print("DB is connectd succesfully (·_·) ···")
        break

    # If there is an error on the connection
    except Exception as error:
        print("Connection to DB failed")
        print("Error:", error)

        #If the connection fails every 2 it will try to reconnect again
        time.sleep(2)

# For the main file to have access to the users and postas components
app.include_router(posts.router)
app.include_router(users.router)


# Path to the api home
@app.get("/")
async def root():
    return {"message": "Wellcome to my Ultimavive Api"}



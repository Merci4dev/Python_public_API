# Modules import
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from sqlalchemy.orm import Session
from . import models
from . database import engine,  get_db


# this line crate the table whe we run the code
models.Base.metadata.create_all(bind=engine)


# Fastapi instantiation
app = FastAPI()

# Defining a basic model for the posts. throw this mode we make the validation for the data we want to recive
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # Adding Optional values to the model
    # rating: Optional[int] = None

# Handel the database connection hard coded
while True:
    try:
        conn = psycopg2.connect(host="hostName",database="dbName", user="userName", password="pass", cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print("DB is connectd succesfully (·_·) ···")
        break

    # If there is an error on the connection
    except Exception as error:
        print("Connection to DB failed")
        print("Error:", error)

        #If the connection fails every 2 it will try to reconnect again
        time.sleep(2)


# Path to the api home
@app.get("/")
async def root():
    return {"message": "Wellcome to my Ultimavive Api"}


# Path to get all Post stored in my_post variable
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):

    # Retrieving all the post fon the databas thew ORM
    posts = db.query(models.Post).all()     
    return {"data": posts}


# Post request to create the posts
@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):

    # Quety to create a post
    # If the model is not to big we can use  this query to create nuw post
    # print(post.dict())
    new_post = models.Post(
        title=post.title, content=post.content, published=post.published)
     
    # If the model have many field we can use  this query to create nuw post
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return  new_post



# Retrieving information from an individual post 
@app.get("/posts/{id}")
def  get_post(id: str, db: Session = Depends(get_db)):

    # Retrieving all the post fon the databas thew ORM
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # Adding validation status code response
    if not post:
   
        # forma dos
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id: {[id]} was not found!")

    return {"Post details": post}



# Handler Delete Function
@app.delete("/posts/{id}", status_code = status.HTTP_404_NOT_FOUND)
def delete_post(id: str, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    # Validation if the id to be deleted does not exist
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {[id]} do not exist")

    # But if the post exists
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_404_NOT_FOUND)
   


# Handler Update Function
@app.put("/posts/{id}")
def update_post(id: str, updated_post: Post, db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    # Validation if the id to be deleted does not exist
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {[id]} do not exist")

    # But if the post exists, we pass the post schema to update it
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    #to return the updated post
    return {"data": post_query.first()}
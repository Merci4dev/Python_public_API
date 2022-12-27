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


# Path to the api home
@app.get("/")
async def root():
    return {"message": "Wellcome to my Ultimavive Api"}


# Path to get all Post stored in my_post variable
# When making a request to all posts we return a list of posts
@app.get("/posts", response_model=List[schemas.Post] )
def get_posts(db: Session = Depends(get_db)):

    # Retrieving all the post fon the databas thew ORM
    posts = db.query(models.Post).all()     
    return posts


# Post request to create the posts
# response_model=schemas.Post (defines the data that we will return to the user when making a request)
@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):

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
@app.get("/posts/{id}", response_model=schemas.Post)
def  get_post(id: str, db: Session = Depends(get_db)):

    # Retrieving all the post fon the databas thew ORM
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # Adding validation status code response
    if not post:
   
        # forma dos
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id: {[id]} was not found!")
    return  post


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
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: str, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    # Validation if the id to be deleted does not exist
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {[id]} do not exist")

    # But if the post exists, we pass the post schema to update it
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
    #to return the updated post
    return post_query.first()



#  Handler User creation Function
@app.post("/users", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOuth)
def create_user( user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Before creating a user we create the encrypted passwd that will be stored in the DB
    hashed_passwd = utils.pwd_hash(user.password)
    user.password = hashed_passwd

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

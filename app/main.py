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
    rating: Optional[int] = None

# Handel the database connection hard coded
while True:
    try:
        conn = psycopg2.connect(host="hostName",database="databaseName", user="userName", password="password", cursor_factory=RealDictCursor)
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
def get_posts():
     
    # Retrieving all the post fon the database
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    print(posts)

    return {"data": posts}


# Post request to create the posts
# Changin the defult stutus code for the raquest
@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):

    # Quety to create a post
    # To avoid sql injection we use the parametizer (%s)
    cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, 
    %s) RETURNING * """, (post.title, post.content, post.published),)

    post = cur.fetchone()
    conn.commit()
    return {"data": post}


# Retrieving information from an individual post 
# THe paht {id} return a string. It must be convert into an integer
# fastapi use (int) to validate tha the id is an integer
@app.get("/posts/{id}")
def get_post(id: str, response: Response):
    cur.execute(""" SELECT * from posts WHERE id = %s """, (str(id),))

    one_post = cur.fetchone()
    # print(one_post)
    # Adding validation status code response
    if one_post == None:
        ## 2 Sending http status code response back with the HTTPException modules
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with id [{id}] not found")

    return {"post_details": one_post}


# Handler Delete Function
@app.delete("/posts/{id}", status_code = status.HTTP_404_NOT_FOUND)
def delete_post(id: str):

    cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))

    deleted_post = cur.fetchone()
    conn.commit()

    # Validation to avoid an error when we want delete a post which do not exists
    if deleted_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id [{id}] do not exists")

    # when we delete a post it will not send any data back
    return Response( status_code = status.HTTP_404_NOT_FOUND)


# Handler Update Function
@app.put("/posts/{id}")
def update_post(id: str, post: Post):
    
    cur.execute("""UPDATE posts SET title = %s, content = %s,  published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))

    updated_post = cur.fetchone()
    conn.commit()
    # varlidation to check if the post do not exists
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {[id]} do not exist")

   
    return {"data": updated_post}
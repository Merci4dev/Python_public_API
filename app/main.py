# Modules import
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time

# Fastapi instantiation
app = FastAPI()

# Defining a basic model for the posts. throw this mode we make the validation for the data we want to recive
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # Adding Optional values to the model
    rating: Optional[int] = None

# Handel the database connection
while True:
    try:
        conn = psycopg2.connect(host="hostName",database="dbName", user="unerName", password="password", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB is connectd succesfully (·_·) ···")
        break

    # If there is an error on the connection
    except Exception as error:
        print("Connection to DB failed")
        print("Error: ", error)

        #If the connection fails every 2 it will try to reconnect again
        time.sleep(2)


# Variable to save posts statically in memory
my_posts = [
    { 
    "title": "Post title No1", "content": "Post content No1", "id": 1,
  },
    { 
    "title": "Post title No2", "content": "Post content No2", "id": 2,
  },
    { 
    "title": "Post title No3", "content": "Post content No3", "id": 3,
  },

]

# function to find a post by its id
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

# Function which manage the logig to finds the index of an especific id into the dict 
def find_index_post(id):
    for i, p, in enumerate(my_posts):
        if p["id"] == id:
            return i
        print(i)
    

# Path to the api home
@app.get("/")
async def root():
    return {"message": "Wellcome to my Ultimavive Api"}


# Path to get all Post stored in my_post variable
@app.get("/posts")
def get_posts():
    
    # when we pass them an array, fastapi will serialize this array into the json format
   return {"data": my_posts}


# Post request to create the posts
# Changin the defult stutus code for the raquest
@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):

    # convertin the pydendic model into a dict
    post_dict= post.dict()

    # adding a random id to aech post
    post_dict["id"] = randrange(100000, 1000000)
   
    # Insert into the the array the new created post
    my_posts.append(post_dict)

    return {"data": post_dict}


# Retrieving information from an individual post 
# THe paht {id} return a string. It must be convert into an integer
# fastapi use (int) to validate tha the id is an integer
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    print(type(id))

    # search for an id and convert is in an ingeger
    post = find_post(int(id))
    print(type(id))

    # Adding validation status code response
    if not post:
        ## 2 Sending http status code response back with the HTTPException modules
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with id [{id}] not found")


        ## 1 Sending http status code response back with the status modules
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id [{id}] not found"}

    return {"post_details": post}



# Handler Delete Function
@app.delete("/posts/{id}", status_code = status.HTTP_404_NOT_FOUND)
def delete_post(id: int):
    index = find_index_post(id)

    # Validation to avoid an error when we want delete a post which do not exists
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id [{id}] do not exists")

    my_posts.pop(index)
    # when we delete a post it will not send any data back
    return Response( status_code = status.HTTP_404_NOT_FOUND)


# Handler Update Function
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # print(post)  
    # check for the post index
    index = find_index_post(id)

    # varlidation to check if the post do not exists
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id [{id}] do not exists")

    # if th post exists conver the data that we recive fron the client to a dict
    post_dict = post.dict()
    # insert the found id into the dict
    post_dict["id"] = id
    # we pass the to new dict to the variable my_post
    my_posts[index] = post_dict

    return {"data": post_dict }
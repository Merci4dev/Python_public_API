# Modules import
from fastapi import Body, FastAPI
from pydantic import BaseModel
from typing import Optional
from random import randrange

# Fastapi instantiation
app = FastAPI()

# Defining a basic model for the posts. throw this mode we make the validation for the data we want to recive
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # Adding Optional values to the model
    rating: Optional[int] = None


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

# function that finds the index of a post
    

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
# The data willbe send throw the requeste boby
@app.post("/posts")
def create_posts(post: Post):

    # convertin the pydendic model into a dict
    post_dict= post.dict()

    # adding a random id to aech post
    post_dict["id"] = randrange(100000, 1000000)
   
    # Insert into the the array the new created post
    my_posts.append(post_dict)

    return {"data": post_dict}
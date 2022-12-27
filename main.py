# Modules import
from fastapi import Body, FastAPI
from pydantic import BaseModel
from typing import Optional

# Fastapi instantiation
app = FastAPI()

# Defining a basic model for the posts. throw this mode we make the validation for the data we want to recive
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # Adding Optional values to the model
    rating: Optional[int] = None
    

# Path to the api home
@app.get("/")
async def root():
    return {"message": "Wellcome to my Ultimavive Api"}


# Path to get all Post
@app.get("/posts")
def get_posts():
   return {"data": "This my List Post"}


# Post request to create the posts
# The data willbe send throw the requeste boby
@app.post("/posts")
def create_posts(post: Post):
    # print(post.title)
    # print(post.content)
    # print(post.rating)
    # print(type(post.rating))
    # print(post)
    ## Here the variable post is a pydentic model
    # print(type(post))

    print("***************************")
    # With the dict method we convert the pydentic model into a dictionary
    # print(post.dict())
    print(post.dict())
    print(type(post.dict()))

    # return {"data","neww post"} ## rerturn an array
    # return {"data": "neww post"}
    return {"data": post}
from pydantic import BaseModel
from datetime import datetime

# Defining a basic model for the posts. throw this mode we make the validation for the data we want to recive from the users
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
   

# la clase CreatePost eredare del la clse padre PostBase
class PostCreate(PostBase):
   pass

#This class handle the filed which must be send basck als response whe we make any request (inherits the fields from PostBase)
class Post(PostBase):
    id: int
    created_at : datetime

    # Convierte el sqlalchemy model en python dict
    class Config:
        orm_mode = True
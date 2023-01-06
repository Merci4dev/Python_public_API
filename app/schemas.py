from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic.types import conint

# Defining a basic model for the posts. throw this mode we make the validation for the data we want to recive from the users
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
   

# la clase CreatePost eredare del la clse padre PostBase
class PostCreate(PostBase):
   pass

   # Defining which data we send back to the user. With this we prevent the password from being returned
class UserOuth(BaseModel):
    id: UUID
    email: EmailStr
    created_at : datetime

    class Config:
        orm_mode = True
        

#This class handle the filed which must be send basck als response whe we make any request (inherits the fields from PostBase)
class Post(PostBase):
    id: UUID
    created_at : datetime
    owner_id: UUID
    owner: UserOuth

    # Convierte el sqlalchemy model en python dict
    class Config:
        orm_mode = True


# Schema for the JOIN
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


# USER SECTION
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# Schema for the user Login
class UsserLogin(BaseModel):
    email : EmailStr
    password: str

# Establishing a schema for the token
class Tocken(BaseModel):
    access_token : str
    token_type : str



# Establishing a schema for the token data
class TokenData(BaseModel):
    id: Optional[str] = None

# Setting the votes schema (likes sistem)
class Votes(BaseModel):
    post_id : UUID
    dir: conint(le=1) # all les dan 1 is allowed

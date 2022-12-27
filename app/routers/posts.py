# POST COMPONENT
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from .. database import get_db


#Define a prefix to the routes
router = APIRouter(
    prefix="/posts",

    # Add a tag to the post group for the docs (http://127.0.0.1:8000/docs)
    tags=["Posts"]
)


# Path to get all Post stored in my_post variable
# When making a request to all posts we return a list of posts
@router.get("/", response_model=List[schemas.Post] )
def get_posts(db: Session = Depends(get_db)):

    # Retrieving all the post fon the databas thew ORM
    posts = db.query(models.Post).all()     
    return posts


# Post request to create the posts
# response_model=schemas.Post (defines the data that we will return to the user when making a request)
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
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
@router.get("/{id}", response_model=schemas.Post)
def  get_post(id: str, db: Session = Depends(get_db)):

    # Retrieving all the post fon the databas thew ORM
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # Adding validation status code response
    if not post:
   
        # forma dos
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id: {[id]} was not found!")
    return  post


# Handler Delete Function
@router.delete("/{id}", status_code = status.HTTP_404_NOT_FOUND)
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
@router.put("/{id}", response_model=schemas.Post)
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


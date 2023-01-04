# POST COMPONENT
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, oauth2
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
def get_posts(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    # Logic to get only the posts corresponding to the logged  user
    # posts = db.query(models.Post).filter(
    #     models.Post.owner_id == current_user.id).all()



    # y limitamos el numero de post que quermos mostrar por pabinacion. tambien lo implementamos el skip (para la paginacion). implemtamos el search params
    # %20 (espacio en la url). Se usa para buscar query con espacios j
   
        # models.Post.title.contains(search)).limit(limit).offset(skip).all()
    

    # Logic to retriev all the post fon the databas 
    posts = db.query(models.Post).all()  

    
    if not posts:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"No posts founded!!")   
    
    return posts


# Post request to create the posts
# oauth2.get_current_user). Force the user to be loged
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),current_user: str = Depends(oauth2.get_current_user)):

    # Quety to create a post
    # If the model is not to big we can use  this query to create nuw post
    # print(get_current_user.id)
     
    # here we spred the owner id into the schema to add a user id to eacht post
    new_post = models.Post(owner_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post


# Retrieving information from an individual post 
@router.get("/{id}", response_model=schemas.Post)
def  get_post(id: str, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    # Retrieving all the post fon the databas thew ORM
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # Adding validation status code response
    if not post:
        # forma dos
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id: {[id]} was not found!")


    # Logic so that the user could not get individual posts . ist usefull for privacity
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this request action")

    return  post


# Handler Delete Function
@router.delete("/{id}", status_code = status.HTTP_404_NOT_FOUND)
def delete_post(id: str, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    

    # Validation if the id to be deleted does not exist
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {[id]} do not exist")

    # Logic so that the user could not delete a post that does not correspond to him
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this Delete request action")

    # But if the post exists
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_404_NOT_FOUND)
   

# Handler Update Function
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: str, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    # Validation if the id to be deleted does not exist
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {[id]} do not exist")

    # Logic so that the user could not update a post that does not correspond to him
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this Update request action")

    # But if the post exists, we pass the post schema to update it
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
    #to return the updated post
    return post_query.first()



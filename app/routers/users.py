# USERS COMPONENT
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from .. database import get_db


# Setting up the router for the Users component
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#  Handler User creation Function
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOuth)
def create_user( user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Before creating a user we create the encrypted passwd that will be stored in the DB
    hashed_passwd = utils.pwd_hash(user.password)
    user.password = hashed_passwd

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


# to handle specific information about a user
# response_model=schemas.UserOuth (prevents that when calling a user id it returns the passwd )
@router.get("/{id}", response_model=schemas.UserOuth)
def get_user(id: str, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()

    # validation
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User id Ivalid")
    
    return user

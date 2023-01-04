from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
# import json


router = APIRouter(tags=["Authentication"])

#Login funtion
# schemas.Tocken. Set which data we will send when we create a new token
@router.post("/login", response_model= schemas.Tocken)
def login( user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):


    user = db.query(models.Users).filter(
        # models.Users.email == user_credentials.email).first()
        models.Users.email == user_credentials.username).first()

    # If the user is not found send this error
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # If the password ar not the same send this error
    if not utils.veriry(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")


    # id_str = str(user.id)
    # js_id = json.dumps(id_str)

    # create token. data represent the data we put into the payload and we will encode the user id to set the data. could be the email too 
    access_token = oauth2.create_access_token(data = {"user_id":str(user.id)})

    # teturn token
    return {"access_token":  access_token, "token_type": "bearer"}
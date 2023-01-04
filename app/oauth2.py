
# FILE maneja todo lo que tiene que ver con jwt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import  Session
from .config import settings

# Make reference to the loging url
oauth2_schema = OAuth2PasswordBearer(tokenUrl = 'login')

# # # Secret Key
SECRET_KEY = "secret_key"

# # # Algoritmo to use
ALGORITHM = "HS256"

# # # Espiration time
ACCESS_TOKEN_EXPIRE_MINUTES = 15


# Funtion to create the jwt access token
def create_access_token(data : dict):
    to_encode = data.copy()

    # # Set the expiraation time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
     # Encode the variacle expire
    to_encode.update({"exp": expire})

    # Set the data we will put into the payload
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) 

    return encoded_jwt


# Function to verifie the access token. Decode JWT and extract the id, validate with the schema the actual token
def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Loock into the auth for the user_id  to extract it
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        # validate that the token match with the schema token
        token_data = schemas.TokenData(id = id)

    except JWTError:
        raise credentials_exception
    
    return token_data


# funtion to  get the current user fron the DB
def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):
    credentials_exception  = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f'Could not Validate credentials', 
        headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.Users).filter(models.Users.id == token.id).first()

    # print(user.email)

    return user
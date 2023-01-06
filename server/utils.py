# This file stores app utilities (like passwd encryption)

# For password encryption
from passlib.context import CryptContext

# Defining the type of encryption we will use
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def pwd_hash(password: str):
    return pwd_context.hash(password)

# Funtion to compare the the password and the hashed password at the DB
def veriry(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Setings for for the enviroment varibales whit pydantic
from pydantic import BaseSettings

# providing the variable that we need to set
class Settings(BaseSettings):
    database_hostname : str
    database_port : str
    database_password : str 
    database_name : str
    database_username : str
    secret_key : str 
    algorithm: str
    access_token_expire_minutes: int

    #import the variable from the .env file
    class Config:
        env_file = ".env"

settings = Settings()
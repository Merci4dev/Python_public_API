# This file handle the database connection and the ORM. This driver is required too ( psycopg2-binary)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import psycopg2
from psycopg2.extras import RealDictCursor 
from .config import settings

# Url which reference the database (for the connection). 
# SQLALCHEMY_DATABASE_URL = "postgresql://userName:passwd@hostName/dbName"

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# The engine is responsable to connect the ORM(sqlalchemy) to postgres
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# Create a session for the connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class from where  all the model tha we create will extend.
Base = declarative_base()

# Dependency for the section for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


'''
# Handel the database connection hard coded
while True:
    try:
        conn = psycopg2.connect(host="hostname",database="dbName", user="userName", password="passwd", cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print("DB is connectd succesfully (·_·) ···")
        break

    # If there is an error on the connection
    except Exception as error:
        print("Connection to DB failed")
        print("Error:", error)

        #If the connection fails every 2 it will try to reconnect again
        time.sleep(2)
'''
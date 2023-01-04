# This file handle the database connection and the ORM. This driver is required too ( psycopg2-binary)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Url which reference the database (for the connection). 
SQLALCHEMY_DATABASE_URL = "postgresql://userName:passwd@hostName/dbName"


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
# each model represent a table in the database. Esto seria la estructura del un ORM
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

from uuid import uuid4
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


# model to create the posts table with sqlalchemy. 
# Note if we make any chage in the table sqlalchemy will no track those chages
class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid4, unique=True)
    
    title = Column(String,  nullable=False) 
    content = Column(String,  nullable=False) 
    published = Column(Boolean, server_default="TRUE",  nullable=False) 
    created_at = Column(TIMESTAMP(timezone=True), 
        nullable=False,  server_default=text('now()')) 
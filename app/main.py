# Modules import
from fastapi import FastAPI
from . import models
from . database import engine
from .routers import posts, users, auth, votes

# this line crate the table whe we run the code
models.Base.metadata.create_all(bind=engine)

# Fastapi instantiation
app = FastAPI()

# url to the components. The main file get  access to the users, auth and posts components
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


# Path to retrieve the api home page
@app.get("/")
async def root():
    return {"message": "Wellcome to my Ultimavive Python Api (·_·)"}


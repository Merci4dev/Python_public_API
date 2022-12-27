# Modules import
from fastapi import Body, FastAPI
from fastapi.params import Body

# Fastapi instantiation
app = FastAPI()


# Path to the api home
@app.get("/")
async def root():
    return {"message": "Wellcome to my Ultimavive Api"}


@app.get("/posts")
def get_posts():
   return {"data": "This my List Post"}


# Post request to create the posts
# The data willbe send throw the requeste boby
@app.post("/posts")
# Extrae la data del cuerpo de la request y lo convierte en un dicionario y lo guarda en la variable payload
def create_posts(payload: dict = Body(...)):
    print(payload)
    print(type(payload))
    return {"data": "Post successfully created"}
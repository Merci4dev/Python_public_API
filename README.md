# Public API built with python, postgresql, fastapi, SQLAlchemy...

# Instructions to run this API
    1 Create a virtual environment 
        virtualenv -p python3 env 

    2 Clone the repository
        https://github.com/Merci4dev/Python-public-API.git
    
    3 Install dependencies
        pip install requirements.txt

    4 Change the database connection values ​​on line 25 of main.py

    5 run the api
        uvicorn app.main:app --reload

    PATH
        Api home
            http://localhost:8000/
        
        Api posts
            http://localhost:8000/posts
        
        Api documentacion
        http://localhost:8000/docs
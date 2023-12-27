from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    id: int
    username: str
    name: str
    surname: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "juliomachin":{
        "id": 1,
        "username":"juliomachin",
        "name": "Julio",
        "surname": "Machin Ruiz",
        "email": "ju.machin@gmail.com",
        "disabled": False,
        "password": "123456"
    },
    "pablo":{
        "id": 1,
        "username":"pablomachin",
        "name": "Pablo",
        "surname": "Machin Ruiz",
        "email": "pa.machin@gmail.com",
        "disabled": True,
        "password": "123456"
    }
}

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=401 , detail="Unauthorized, CREDENTIALS NOT VALID", headers={"WWW-Authenticate": "Bearer"})
    
    if user.disabled == True:
        raise HTTPException(status_code=401 , detail="User not avaliable yet!", headers={"WWW-Authenticate": "Bearer"})
    return user

@app.post("/login", response_description="Authenticated" ,status_code=201)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="The user is not register")

    user = search_userDB(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=401, detail="The password is not correct")
    
    return { "access_token": user.username , "token_type": "bearer"}

@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

def search_userDB(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])    

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()


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
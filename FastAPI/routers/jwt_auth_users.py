from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta



ALGORITHM = "HS256"
ACCESS_TOKEN_TIME = 1
#openssl rand -hex 32
SECRET = "a3eecf969462c2dd3500bdac78ecb2f223740b95a189d5096772d024f127db0a"

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

router = APIRouter(prefix="/jwtauth",
                   tags=["jwtauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

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
        "password": "$2a$12$Ur1EWkTT7HxckQXGpYuKbeQI7PnHuy9wnFH8ZMLyW9zEwfDedfy66"
    },
    "pablomachin":{
        "id": 1,
        "username":"pablomachin",
        "name": "Pablo",
        "surname": "Machin Ruiz",
        "email": "pa.machin@gmail.com",
        "disabled": False,
        "password": "$2a$12$6d1QMzIca/lax8qKFNE.JOkDbH5lKuVPHbuhiUXgTxku06VLac2Zu"
    }
}

async def auth_user(token: str = Depends(oauth2)):

    exception_Unauthorized =  HTTPException(status_code=401 , detail="Unauthorized, CREDENTIALS NOT VALID", headers={"JWT-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")
        if username is None:
            raise exception_Unauthorized
        
    except JWTError:
        raise exception_Unauthorized

    return search_user(username)



async def current_user(user: User = Depends(auth_user)):

    if user.disabled == True:
        raise HTTPException(status_code=401 , detail="User not avaliable yet!", headers={"WWW-Authenticate": "Bearer"})
    return user



@router.post("/login", response_description="Authenticated" ,status_code=201)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="The user is not register")

    user = search_userDB(form.username)

    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=401, detail="The password is not correct")
    else:
        access_token_expiration = timedelta(minutes=ACCESS_TOKEN_TIME)

        expire = datetime.utcnow() + access_token_expiration

        access_token = {"sub": user.username, 
                        "exp": expire}
        
        return { "access_token_jwt":  jwt.encode( access_token, SECRET ,algorithm=ALGORITHM) , "token_type": "bearer"}


def search_userDB(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username]) 
    
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

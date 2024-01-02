from fastapi import FastAPI
from routers import films, jwt_auth_users, basic_auth_users, films_db


#Start server
#python -m uvicorn main:app --reload

#Documentation
#http://127.0.0.1:8000/docs

app = FastAPI()

app.include_router(films.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(films_db.router)


@app.get("/")
def read_root():
    return {"API de PELICULAS"}

from fastapi import FastAPI
from routers import films


#Start server
#python -m uvicorn main:app --reload

#Documentation
#http://127.0.0.1:8000/docs

app = FastAPI()

app.include_router(films.router)


@app.get("/")
def read_root():
    return {"API de PELICULAS"}

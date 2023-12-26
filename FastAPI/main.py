from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union


app = FastAPI()

class Film(BaseModel):
    id: int
    titulo: str
    director: str
    puntuacion: float
    nacionalidad: str

films_list = [Film(id=1,titulo= "The First Slam Dunk (2022)",director= "Takehiko Inoue",puntuacion= 7.8, nacionalidad= "Japón" ),
              Film(id=2, titulo= "As bestas (2022)", director="Rodrigo Sorogoyen",puntuacion= 7.6,nacionalidad= "España"),
              Film(id=3, titulo="El regreso de las golondrinas (2022)",director="Li Ruijun", puntuacion= 7.6, nacionalidad="China")]




@app.get("/usersjson")
async def peliculasjson():
    return[{
      "id": "1",
      "titulo": "The First Slam Dunk (2022)",
      "director": "Takehiko Inoue",
      "puntuacion": 7.8,
      "nacionalidad": "Japón"
    },
    {
      "id": "2",
      "titulo": "As bestas (2022)",
      "director": "Rodrigo Sorogoyen",
      "puntuacion": 7.6,
      "nacionalidad": "España"
    },
    {
      "id": "3",
      "titulo": "El regreso de las golondrinas (2022)",
      "director": "Li Ruijun",
      "puntuacion": 7.6,
      "nacionalidad": "China"
    }]


@app.get("/")
def read_root():
    return {"API de PELICULAS"}

@app.get("/films")
async def films ():
    return films_list

@app.get("/films/")
async def films (id: int):
    return search_films

@app.get("/films/{id}")
def search_films(id: int):
    return search_films(id)

@app.get("/filmsquery/")
async def films(id: int):
    return search_films(id)

@app.post("/addfilm/")
async def add_film(newFilm: Film):
    if type(search_films(newFilm.id)) == Film:
        return { "error": "This film arlready exists"}
    else:
        films_list.append(newFilm)


def search_films(id: int):
    films = filter(lambda film: film.id == id, films_list)
    try:
        return list(films)[0]
    except:
        return { "error": "Not found this film"}

def add_film(newFilm: Film):
    films_list.append(newFilm)
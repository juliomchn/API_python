from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Union

router = APIRouter()

class Film(BaseModel):
    id: int
    titulo: str
    director: str
    puntuacion: float
    nacionalidad: str

films_list = [Film(id=1,titulo= "The First Slam Dunk (2022)",director= "Takehiko Inoue",puntuacion= 7.8, nacionalidad= "Japón" ),
              Film(id=2, titulo= "As bestas (2022)", director="Rodrigo Sorogoyen",puntuacion= 7.6,nacionalidad= "España"),
              Film(id=3, titulo="El regreso de las golondrinas (2022)",director="Li Ruijun", puntuacion= 7.6, nacionalidad="China")]




@router.get("/usersjson")
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


@router.get("/films")
async def films ():
    return films_list

@router.get("/films/")
async def films (id: int):
    return search_films

@router.get("/films/{id}")
def search_films(id: int):
    return search_films(id)

@router.get("/filmsquery/")
async def films(id: int):
    return search_films(id)

@router.post("/addfilm/",response_model= Film ,status_code=201)
async def add_film(newFilm: Film):
    if type(search_films(newFilm.id)) == Film:
        raise HTTPException(status_code=404, detail="This film already exists")
    else:
        return add_film(newFilm)

@router.put("/updatefilm/")
async def update_film(newFilm: Film):
    return update_film(newFilm)

@router.delete("/deletefilm/{id}")
async def delete_film(id: int):
    return delete_film(id)


def update_film(updateFilm: Film): 
    for i, f in enumerate(films_list):
        if f.id == updateFilm.id:
            films_list[i] = updateFilm
            found = True

    if not found:
        return { "error": "Not found this film"}
    else:
        return updateFilm
    
def delete_film(id: int):
    for i, f in enumerate(films_list):
        if f.id == id:
            del films_list[i]
            found = True
        
    if not found: 
       return { "error": "Not found this film"}
    else:
        return { "Deleted film succesfully!"}



def search_films(id: int):
    films = filter(lambda film: film.id == id, films_list)
    try:
        return list(films)[0]
    except:
        return { "error": "Not found this film"}

def add_film(newFilm: Film):
    films_list.append(newFilm)
    return newFilm
from fastapi import APIRouter, HTTPException,  status
from db.models.film import Film
from db.schemas.film import film_schema, films_schema
from db.dbConnection import db_connection
from bson import ObjectId


router = APIRouter(prefix="/db", tags=["filmDB"], responses={status.HTTP_404_NOT_FOUND : {"message" : "Not found"}})



@router.get("/films", response_model=list[Film])
async def films ():
    return films_schema(db_connection.films.find())


@router.get("/films/{id}")
def search_films(id: str):
    return search_films("_id",ObjectId(id))


@router.post("/addfilm",response_model= Film ,status_code= status.HTTP_201_CREATED)
async def add_film(film: Film):

    if type(search_films("titulo", film.titulo)) == Film:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The Film already exists")
    
    film_dict = dict(film)
    del film_dict["id"]

    id = db_connection.films.insert_one(film_dict).inserted_id

    new_film = film_schema(db_connection.films.find_one({"_id": id}))

    return Film(**new_film)

@router.put("/updatefilm/", response_model= Film ,status_code= status.HTTP_201_CREATED)
async def update_film(film: Film):

    film_dict = dict(film)
    del film_dict["id"]

    try:
        db_connection.films.find_one_and_replace({"_id": ObjectId(film.id)}, film_dict)
    except:
        return { "error": "Not found this film"}
    
    return search_films("_id", ObjectId(film.id) )


@router.delete("/deletefilm/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_film(id: str):
    
    found = db_connection.films.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return { "error": "Not delete this film."}
    


def search_films(field: str, key ):
    try:
        film = film_schema(db_connection.films.find_one({field: key}))
        return Film(**film)
    
    except:
        return { "error": "Not found this film"}

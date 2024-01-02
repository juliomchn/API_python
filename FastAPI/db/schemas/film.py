def film_schema(film) -> dict:
    return {"id": str(film["_id"]),
            "titulo": film["titulo"],
            "director": film["director"],
            "puntuacion": str(film["puntuacion"]),
            "nacionalidad": film["nacionalidad"]
            }
    
def films_schema(films) -> list:
    return [film_schema(film) for film in films]
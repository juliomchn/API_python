from pydantic import BaseModel
from typing import Optional

class Film(BaseModel):
    id: Optional[str]
    titulo: str
    director: str
    puntuacion: float
    nacionalidad: str
"""Modelos de datos: describen los campos de los artistas y cómo se validan."""
from pydantic import BaseModel, Field


class ArtistaNuevo(BaseModel):
    nombre_artistico: str = Field(min_length=1)
    nombre_real: str
    genero_musical: str
    fecha_nacimiento: str
    fecha_murio: str | None = None
    discos_vendidos: str
    descripcion_breve: str
    origen_pais: str
    discografica: str
    cancion_mas_famosa: str
    redes: str
    activo: bool

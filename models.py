"""Modelos de datos: describen qué campos tiene cada elemento y cómo se validan."""
from pydantic import BaseModel, Field


# CAMBIAR: los campos del objeto X de tu proyecto (mascota, equipo, libro, etc.).
# El campo "id" no va acá: lo asigna la base de datos (db.py) al agregar.
class ItemNuevo(BaseModel):
    nombre: str = Field(min_length=1)
    descripcion: str = ""
    cantidad: int = Field(ge=0)

"""API base con FastAPI: listar, ver uno y agregar elementos de un objeto X.

Para adaptarla al proyecto propio, buscar los comentarios que empiezan con
"CAMBIAR" (en main.py, models.py y db.py) y reemplazar "item" por el objeto elegido.
"""
import os
import secrets

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Response, Security
from fastapi.security import APIKeyHeader

import db
from models import ItemNuevo

load_dotenv()  # lee las variables del archivo .env (solo en la computadora local)
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    print("AVISO: no hay API_KEY configurada. Los endpoints protegidos devolverán 401.")

app = FastAPI(
    title="API de items",  # CAMBIAR: nombre de la API
    description="Plantilla base: listar, ver uno y agregar (con API Key).",
    version="1.0.0",
)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


# ---------- Seguridad ----------
def verificar_api_key(clave: str | None = Security(api_key_header)):
    print(clave)
    print(API_KEY)
    if clave is None or API_KEY is None:
        raise HTTPException(status_code=401, detail="API Key inválida o ausente")
    if not secrets.compare_digest(clave.encode(), API_KEY.encode()):
        raise HTTPException(status_code=401, detail="API Key inválida o ausente")


# ---------- Endpoints ----------
@app.get("/")
def inicio():
    return {"mensaje": "API funcionando"}


# CAMBIAR: la ruta /items y los nombres de las funciones
@app.get("/items")
def listar_items(buscar: str | None = None):
    items = db.cargar_items()
    print(items)
    if buscar:
        items = [i for i in items if buscar.lower() in i["nombre_artistico"].lower()]
    return items


@app.get("/items/{item_id}")
def ver_item(item_id: int):
    item = db.buscar_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return item

@app.post("/artistas", status_code=201, dependencies=[Depends(verificar_api_key)])
def agregar_artista(nuevo: ArtistaNuevo):
    return db.agregar_artista(nuevo.model_dump())


@app.put(
    "/artistas/{artista_id}",
    dependencies=[Depends(verificar_api_key)],
)
def actualizar_artista(artista_id: int, artista_actualizado: ArtistaNuevo):
    artista = db.actualizar_artista(
        artista_id, artista_actualizado.model_dump()
    )
    if artista is None:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    return artista

# Este metodo hace que puedas eliminar un artista de la base de datos mediante el ApiDog
@app.delete(
    "/artistas/{artista_id}",
    status_code=204,
    dependencies=[Depends(verificar_api_key)],
)
def eliminar_artista(artista_id: int):
    eliminado = db.eliminar_artista(artista_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    return Response(status_code=204)

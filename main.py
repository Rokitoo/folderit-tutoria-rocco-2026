"""API base con FastAPI: listar, ver uno y agregar elementos de un objeto X.

Para adaptarla al proyecto propio, buscar los comentarios que empiezan con
"CAMBIAR" (en main.py, models.py y db.py) y reemplazar "item" por el objeto elegido.
"""
import os
import secrets

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Security
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
    if buscar:
        items = [i for i in items if buscar.lower() in i["nombre"].lower()]
    return items


@app.get("/items/{item_id}")
def ver_item(item_id: int):
    item = db.buscar_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return item


@app.post("/items", status_code=201, dependencies=[Depends(verificar_api_key)])
def agregar_item(nuevo: ItemNuevo):
    return db.agregar_item(nuevo.model_dump())

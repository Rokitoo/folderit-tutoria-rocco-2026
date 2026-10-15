"""API de artistas con FastAPI: listar, ver uno y agregar artistas.

Los endpoints delegan el acceso a los datos a las funciones de db.py.
"""
import os
import secrets

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader

import db
from models import ArtistaNuevo

load_dotenv()  # lee las variables del archivo .env (solo en la computadora local)
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    print("AVISO: no hay API_KEY configurada. Los endpoints protegidos devolverán 401.")

app = FastAPI(
    title="API de artistas",
    description="Lista, consulta y agrega artistas.",
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


@app.get("/artistas")
def listar_artistas(buscar: str | None = None):
    artistas = db.cargar_artistas()
    if buscar:
        artistas = [
            artista
            for artista in artistas
            if buscar.lower() in artista["nombre_artistico"].lower()
        ]
    print(artistas)    
    if len(artistas) == 0:
         raise HTTPException(status_code=404, detail="Artista no encontrado")   
    return artistas


@app.get("/artistas/{artista_id}")
def ver_artista(artista_id: int):
    artista = db.buscar_artista(artista_id)
    if artista is None:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    return artista


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

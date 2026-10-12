"""Base de datos simulada: guarda los datos en un archivo JSON.

Todo el acceso a los datos está en este archivo. Los endpoints de main.py solo
llaman a estas funciones, sin saber dónde ni cómo se guardan. Más adelante se
puede reemplazar este archivo por una base de datos real sin tocar main.py.
"""
import json
from pathlib import Path

# CAMBIAR (opcional): nombre del archivo de datos
ARCHIVO = Path(__file__).parent / "datos.json"


def cargar_items():
    """Lee el archivo y devuelve la lista de elementos."""
    if not ARCHIVO.exists():
        return []
    return json.loads(ARCHIVO.read_text(encoding="utf-8"))


def guardar_items(items):
    """Escribe la lista completa de elementos en el archivo."""
    texto = json.dumps(items, ensure_ascii=False, indent=2)
    ARCHIVO.write_text(texto, encoding="utf-8")


def buscar_item(item_id):
    """Devuelve el elemento con ese id, o None si no existe."""
    for item in cargar_items():
        if item["id"] == item_id:
            return item
    return None


def agregar_item(datos):
    """Agrega un elemento nuevo (diccionario sin id), le asigna un id y lo devuelve."""
    items = cargar_items()
    nuevo_id = max((i["id"] for i in items), default=0) + 1
    item = {"id": nuevo_id, **datos}
    items.append(item)
    guardar_items(items)
    return item

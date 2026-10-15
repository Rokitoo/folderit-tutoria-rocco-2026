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

def agregar_artista(datos: dict[str, Any]) -> dict[str, Any]:
    """Inserta un artista y devuelve la fila creada por Supabase."""
    response = (
        _obtener_cliente()
        .table(TABLA_ARTISTAS)
        .insert(datos)
        .execute()
    )
    if not response.data:
        raise RuntimeError("Supabase no devolvió el artista insertado.")
    return response.data[0]


def actualizar_artista(
    artista_id: int, datos: dict[str, Any]
) -> dict[str, Any] | None:
    """Reemplaza los datos del artista y devuelve la fila actualizada, si existe."""
    response = (
        _obtener_cliente()
        .table(TABLA_ARTISTAS)
        .update(datos)
        .eq("id", artista_id)
        .execute()
    )
    return response.data[0] if response.data else None


def eliminar_artista(artista_id: int) -> bool:
    """Elimina al artista indicado y devuelve si existía."""
    cliente = _obtener_cliente()
    existente = buscar_artista(artista_id)
    if existente is None:
        return False

    cliente.table(TABLA_ARTISTAS).delete().eq("id", artista_id).execute()
    return True

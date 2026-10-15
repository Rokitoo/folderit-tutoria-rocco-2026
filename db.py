"""Acceso a la tabla de artistas en Supabase.

Los endpoints de main.py usan estas funciones para consultar y guardar artistas.
"""
from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from supabase import Client

TABLA_ARTISTAS = "Artistas"
_cliente: Client | None = None


def _obtener_cliente() -> Client:
    """Crea el cliente de Supabase la primera vez que se necesita."""
    global _cliente
    if _cliente is None:
        url = os.getenv("SUPABASE_URL")
        clave = os.getenv("SUPABASE_KEY")
        if not url or not clave:
            raise RuntimeError(
                "Faltan SUPABASE_URL o SUPABASE_KEY en la configuración."
            )
        from supabase import create_client

        _cliente = create_client(url, clave)
    return _cliente


def cargar_artistas() -> list[dict[str, Any]]:
    """Devuelve todos los artistas guardados en Supabase."""
    response = _obtener_cliente().table(TABLA_ARTISTAS).select("*").execute()
    return response.data


def buscar_artista(artista_id: int) -> dict[str, Any] | None:
    """Devuelve el artista con ese id, o None si no existe."""
    response = (
        _obtener_cliente()
        .table(TABLA_ARTISTAS)
        .select("*")
        .eq("id", artista_id)
        .limit(1)
        .execute()
    )
    return response.data[0] if response.data else None


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

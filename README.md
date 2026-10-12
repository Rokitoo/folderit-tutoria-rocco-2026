# Plantilla de API con FastAPI

Proyecto base listo para correr: una API con listar, ver uno y agregar elementos de un objeto genérico (`item`), datos guardados en un archivo JSON que simula una base de datos, y protección con API Key. Sirve de punto de partida para el mini proyecto: reemplazar `item` por el objeto elegido (mascota, equipo de fútbol, libro, etc.).

## Qué incluye

| Archivo | Para qué sirve |
|---|---|
| `main.py` | La API: endpoints y verificación de la API Key. |
| `models.py` | El modelo de datos: qué campos tiene cada elemento y cómo se validan. |
| `db.py` | La "base de datos" simulada: funciones para cargar, guardar, buscar y agregar. |
| `datos.json` | Los datos iniciales. |
| `requirements.txt` | Las librerías que necesita el proyecto. |
| `.env.example` | Modelo del archivo `.env` donde va la API Key. |
| `.gitignore` | Evita que Git suba `.venv/` y `.env`. |

Los endpoints de `main.py` no leen ni escriben archivos: llaman a las funciones de `db.py`. Así, si más adelante se usa una base de datos real, solo hay que reemplazar `db.py`.

## Puesta en marcha

Requiere Python 3.10 o superior.

1. Crear y activar el entorno virtual:

   ```
   python -m venv .venv
   ```

   | Sistema | Activar |
   |---|---|
   | Windows (cmd) | `.venv\Scripts\activate` |
   | Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
   | macOS / Linux | `source .venv/bin/activate` |

2. Instalar las librerías:

   ```
   pip install -r requirements.txt
   ```

3. Crear el archivo `.env` a partir del modelo:

   | Sistema | Comando |
   |---|---|
   | Windows | `copy .env.example .env` |
   | macOS / Linux | `cp .env.example .env` |

   Generar una clave y pegarla como valor de `API_KEY` en `.env`:

   ```
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

4. Ejecutar la API:

   ```
   fastapi dev main.py
   ```

5. Abrir en el navegador `http://127.0.0.1:8000/docs`: es la documentación interactiva, donde se puede probar cada endpoint.

## Endpoints

| Método | Ruta | Descripción | Protegido |
|---|---|---|---|
| GET | `/` | Verifica que la API funciona. | No |
| GET | `/items` | Lista todos. Admite `?buscar=texto` para filtrar por nombre. | No |
| GET | `/items/{id}` | Devuelve uno por id (404 si no existe). | No |
| POST | `/items` | Agrega uno nuevo. | Sí, con API Key |

Para probar el POST, enviar el header `X-API-Key` con la clave del `.env`. En `/docs` se usa el botón **Authorize**; en Postman, la pestaña **Headers**. Sin clave (o con una incorrecta), la API responde `401`.

Ejemplo de body para el POST:

```json
{"nombre": "Mi primer item", "descripcion": "Probando la API", "cantidad": 3}
```

## Adaptarla al proyecto propio

Buscar `CAMBIAR` en los archivos para encontrar cada punto a modificar.

1. **Elegir el objeto X** del proyecto y sus campos (por ejemplo, una mascota con nombre, especie y edad).
2. **`models.py`:** reemplazar `ItemNuevo` y sus campos por los del objeto elegido. No incluir el `id`: lo asigna `db.py`.
3. **`datos.json`:** reemplazar los datos de ejemplo por otros con los mismos campos, cada uno con su `id`.
4. **`db.py`:** renombrar las funciones (`cargar_items`, `agregar_item`...) y, si se quiere, el archivo de datos. Si cambia el nombre de un campo, revisar las funciones que lo usan.
5. **`main.py`:** renombrar rutas (`/items`), funciones, el título de la API y el campo por el que filtra `listar_items`.
6. **README:** actualizar la descripción de la API.

## Publicar en un cloud

La API Key **nunca** se sube al repositorio ni a la plataforma dentro de un archivo: se carga como variable secreta en el cloud.

### Con FastAPI Cloud

Con el entorno virtual activo:

```
fastapi login
fastapi deploy
```

Después, cargar la API Key como secreto y volver a desplegar para que la app la tome:

```
fastapi cloud env set --secret API_KEY "la-clave"
fastapi deploy
```

La URL pública aparece al terminar el deploy. Agregar `/docs` al final para ver la documentación.

### Importante sobre los datos

En un cloud, el archivo `datos.json` puede no conservar los datos agregados con POST entre reinicios o redespliegues. Para la demo, tratar esos datos como temporales.

## Errores comunes

| Síntoma | Solución |
|---|---|
| `fastapi` no se reconoce | Activar el entorno virtual (debe verse `(.venv)`) e instalar con `pip install -r requirements.txt`. |
| Siempre `401` con la clave correcta | Revisar que el header se llame `X-API-Key` y que `.env` esté en la carpeta del proyecto. |
| Aviso de `API_KEY` al arrancar | Falta crear el archivo `.env` (paso 3). |
| `ModuleNotFoundError: db` o `models` | Ejecutar `fastapi dev main.py` desde la carpeta del proyecto. |
| Puerto ocupado | Usar otro puerto: `fastapi dev main.py --port 8001`. |

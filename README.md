# API de artistas con FastAPI

API FastAPI para listar, consultar y agregar artistas guardados en Supabase. La creación está protegida con API Key.

## Qué incluye

| Archivo | Para qué sirve |
|---|---|
| `main.py` | La API: endpoints de artistas y verificación de la API Key. |
| `models.py` | El modelo `ArtistaNuevo` y la validación de sus campos. |
| `db.py` | Conexión a Supabase y funciones para consultar y agregar artistas. |
| `seed_artistas.sql` | Inserciones iniciales para cargar en Supabase los artistas de `datos.json`. |
| `requirements.txt` | Las librerías que necesita el proyecto. |
| `.env.example` | Modelo del archivo `.env` con la API Key y las credenciales de Supabase. |
| `.gitignore` | Evita que Git suba `.venv/` y `.env`. |

Los endpoints de `main.py` delegan el acceso a Supabase a las funciones de `db.py`.

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

   Configurar `API_KEY`, `SUPABASE_URL` y `SUPABASE_KEY` en `.env`. La URL y la clave se obtienen desde el panel del proyecto de Supabase. Para generar el valor de `API_KEY`:

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
| GET | `/artistas` | Lista todos. Admite `?buscar=texto` para filtrar por nombre artístico. | No |
| GET | `/artistas/{artista_id}` | Devuelve uno por id (404 si no existe). | No |
| POST | `/artistas` | Agrega un artista nuevo. | Sí, con API Key |
| PUT | `/artistas/{artista_id}` | Reemplaza los datos de un artista existente (404 si no existe). | Sí, con API Key |

Para probar el POST o PUT, enviar el header `X-API-Key` con la clave del `.env`. En `/docs` se usa el botón **Authorize**; en Postman, la pestaña **Headers**. Sin clave (o con una incorrecta), la API responde `401`.

Ejemplo de body para el POST:

```json
{
  "nombre_artistico": "Mi primer artista",
  "nombre_real": "Nombre real",
  "genero_musical": "Pop",
  "fecha_nacimiento": "01/01/2000",
  "fecha_murio": null,
  "discos_vendidos": "Más de 1 millón",
  "descripcion_breve": "Descripción del artista.",
  "origen_pais": "Argentina",
  "discografica": "Discográfica",
  "cancion_mas_famosa": "Mi canción",
  "redes": "Instagram: @artista",
  "activo": true
}
```

El body se usa tanto para POST como para PUT y requiere todos los campos, salvo `fecha_murio`, que puede omitirse o enviarse como `null`. En PUT se reemplazan los datos del artista con el ID indicado; el `id` no se envía en el body.

## Configurar Supabase

Crear una tabla llamada `Artistas` con una columna `id` autogenerada y las columnas de artista usadas en el ejemplo. La tabla debe permitir las operaciones de lectura, escritura y actualización desde la clave configurada en `SUPABASE_KEY`. La API consulta esta tabla para las rutas GET, y guarda o actualiza registros en POST y PUT.

Para cargar los diez registros iniciales de `datos.json`, ejecutar `seed_artistas.sql` en el SQL Editor de Supabase, después de crear la tabla.

## Publicar en un cloud

La API Key **nunca** se sube al repositorio ni a la plataforma dentro de un archivo: se carga como variable secreta en el cloud.

### Con FastAPI Cloud

Con el entorno virtual activo:

```
fastapi login
fastapi deploy
```

Después, cargar estas variables como secretos y volver a desplegar para que la app las tome:

```
fastapi cloud env set --secret API_KEY "la-clave"
fastapi cloud env set --secret SUPABASE_URL "la-url"
fastapi cloud env set --secret SUPABASE_KEY "la-clave-de-supabase"
fastapi deploy
```

La URL pública aparece al terminar el deploy. Agregar `/docs` al final para ver la documentación.

## Errores comunes

| Síntoma | Solución |
|---|---|
| `fastapi` no se reconoce | Activar el entorno virtual (debe verse `(.venv)`) e instalar con `pip install -r requirements.txt`. |
| Siempre `401` con la clave correcta | Revisar que el header se llame `X-API-Key` y que `.env` esté en la carpeta del proyecto. |
| Aviso de `API_KEY` al arrancar | Falta crear el archivo `.env` (paso 3). |
| Error por configuración de Supabase | Revisar que `SUPABASE_URL` y `SUPABASE_KEY` estén configuradas. |
| `ModuleNotFoundError: db` o `models` | Ejecutar `fastapi dev main.py` desde la carpeta del proyecto. |
| Puerto ocupado | Usar otro puerto: `fastapi dev main.py --port 8001`. |

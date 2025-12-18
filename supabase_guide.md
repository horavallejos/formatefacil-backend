# Guía de Implementación Supabase + FastAPI

Este documento resume el procedimiento correcto para integrar Supabase en tu proyecto FastAPI, explica las decisiones técnicas tomadas y lista los errores resueltos.

## 1. Procedimiento Correcto de Implementación

### A. Dependencias ([requirements.txt](file:///d:/1_PROYECTOS/_alexis_formatefacil.online/formatefacil-backend/requirements.txt))
Para evitar conflictos de versiones (específicamente con `httpx` y `gotrue`), es crucial usar versiones compatibles.
*   **Recomendado**: `supabase>=2.9.0`
*   **Comando**:
    ```bash
    pip install supabase==2.9.0
    ```
    *Esto asegura que el cliente soporte los argumentos actuales de `httpx` (resolvió el error de `proxy`).*

### B. Variables de Entorno ([.env](file:///d:/1_PROYECTOS/_alexis_formatefacil.online/formatefacil-backend/.env))
El cliente de Python actual (v2.9.0) requiere las **Keys Legacy** (formato JWT).
*   **Archivo**: [.env](file:///d:/1_PROYECTOS/_alexis_formatefacil.online/formatefacil-backend/.env)
*   **Estructura**:
    ```properties
    SUPABASE_URL="https://tu-proyecto.supabase.co"
    SUPABASE_KEY="eyJhbG..."  <-- Usar la key 'anon' o 'service_role' (JWT), NO la 'sb_secret_'
    ```

### C. Inicialización del Cliente ([main.py](file:///d:/1_PROYECTOS/_alexis_formatefacil.online/formatefacil-backend/main.py))
El código debe inicializar el cliente usando estas variables.
```python
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Inicialización estándar
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
```

## 2. Notas sobre la "Nueva Forma" vs. Actual

La documentación de Supabase menciona nuevas keys (`sb_publishable_...` y `sb_secret_...`).
*   **Situación**: Estas keys son parte de una mejora de seguridad reciente de Supabase.
*   **Limitación Actual**: La librería oficial de Python (`supabase-py`) **aún no soporta nativamente** este nuevo formato en su versión estable actual (v2.9.0). Por eso falla con "Invalid API key".
*   **Por qué usamos la forma "vieja" (JWT)**: Es la única que funciona con el cliente de Python actual hasta que lancen una actualización. Es seguro y estándar para implementaciones actuales.

## 3. Bitácora de Errores y Soluciones

Durante la sesión encontramos y resolvimos los siguientes problemas:

| Error | Causa | Solución |
| :--- | :--- | :--- |
| **`TypeError: ... unexpected keyword argument 'proxy'`** | Conflicto de versiones. La versión vieja de `supabase` (2.4.0) enviaba un argumento `proxy` que la versión nueva de `httpx` ya no acepta. | Actualizar `supabase` a `2.9.0` en [requirements.txt](file:///d:/1_PROYECTOS/_alexis_formatefacil.online/formatefacil-backend/requirements.txt). |
| **`SupabaseException: Invalid API key`** | Se intentó usar la nueva key (`sb_secret_...`) o la key estaba mal copiada/truncada. | Usar la **Key Legacy (JWT)** (empieza con `eyJ...`) obtenida del dashboard. |
| **`NameError / ModuleNotFoundError` (psycopg2)** | Intento de workaround usando `psycopg2` sin las credenciales de conexión directa a BD configuradas. | Volver a la implementación nativa de Supabase (`create_client`) que maneja la conexión vía HTTP/API. |
| **`Connection refused` / `dotenv` parsing error** | El archivo [.env](file:///d:/1_PROYECTOS/_alexis_formatefacil.online/formatefacil-backend/.env) tenía líneas pegadas (mala sintaxis), lo que impedía leer las variables correctamente. | Corregir los saltos de línea en el archivo [.env](file:///d:/1_PROYECTOS/_alexis_formatefacil.online/formatefacil-backend/.env). |

---
**Conclusión**: Tu proyecto ahora corre estable con la versión actualizada del cliente y las credenciales correctas.

from contextlib import contextmanager
from fastapi import Depends, HTTPException
from ..core.events import get_client

@contextmanager
def get_db():
    db_client = get_client()
    if not db_client:
        raise HTTPException(status_code=500, detail="La conexión a la base de datos no está disponible.")
    try:
        yield db_client
    finally:
        pass  # Aquí puedes manejar la lógica de limpieza si es necesario

from ..dataBase.conexion.db_connection import get_db_client
from contextlib import contextmanager
import logging

logger = logging.getLogger("events")
db_client = None

def startup_event():
    global db_client
    try:
        db_client = get_db_client()
        logger.info("Conexión a la base de datos exitosa.")
    except Exception as e:
        logger.error(f"Error al conectar con la base de datos: {e}")
        raise e

def shutdown_event():
    global db_client
    if db_client:
        db_client.close()
        logger.info("Conexión a la base de datos cerrada.")

@contextmanager
def get_db():
    from ..core.events import get_client  # Accede al cliente global
    db_client = get_client()
    if not db_client:
        raise Exception("La conexión a la base de datos no está disponible.")
    try:
        yield db_client
    finally:
        pass  # Aquí puedes manejar la lógica de limpieza si es necesario
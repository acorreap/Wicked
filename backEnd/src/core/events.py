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

def get_client():
    global db_client
    
    return db_client
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from ...core.settings import settings  # Asegúrate de que `settings` tiene la URL de la base de datos.

# Función para obtener el cliente de la base de datos
def get_db_client():
    """
    Inicializa y retorna un cliente de MongoDB.
    """
    uri = settings.DATABASE_URL  # URL de conexión desde el archivo de configuración.
    
    try:
        # Crear el cliente de MongoDB
        client = MongoClient(uri, server_api=ServerApi('1'))
        
        # Verificar la conexión con un 'ping'
        client.admin.command("ping")
        print("Conexión exitosa a MongoDB!")
        
        return client
    except Exception as e:
        print(f"Error al conectar con MongoDB: {e}")
        raise e

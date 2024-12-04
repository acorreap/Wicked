from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str  # Variable obligatoria

    class Config:
        env_file = ".env"  # Ruta del archivo .env
        env_file_encoding = "utf-8"  # Asegura que la codificación sea correcta

# Instancia global
settings = Settings()

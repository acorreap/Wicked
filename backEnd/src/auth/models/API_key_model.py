import secrets
from datetime import datetime, timedelta
from ...core.crypto import manager
from typing import Optional
from bson import ObjectId

class ApiKeyModel:

    def __init__(self, _id: Optional[ObjectId] = None, api_key_hashed: str = "", create_date: Optional[datetime]= None, expiration_date: Optional[datetime] = None, active: Optional[bool] = None):
        self._id = _id or ObjectId()  # Genera un ObjectId único si no se proporciona
        self.api_key_hashed = api_key_hashed
        self.create_date = create_date or datetime.now()
        self.expiration_date = expiration_date or (datetime.now() + timedelta(days=30))
        self.active = active if active is not None else True
    
    @property
    def id(self):
        return self._id

    # Setter para __id
    @id.setter
    def id(self, value: str):
        """
        Setter para el ID, convierte un string a ObjectId si es necesario.
        """
        if not ObjectId.is_valid(value):
            raise ValueError("El ID debe ser un ObjectId válido o una cadena representativa.")
        self._id = ObjectId(value)

    @classmethod
    def generate(cls, validity_period_days: int = 30) -> tuple["ApiKeyModel", str]:
        """
        Genera una nueva API Key con un período de validez especificado.
        """
        raw_api_key = secrets.token_urlsafe(32) 
        api_key_hashed = manager.hash_data(raw_api_key)
        expiration_date = datetime.now() + timedelta(days=validity_period_days)
        return cls(api_key_hashed=api_key_hashed, expiration_date=expiration_date), raw_api_key

    def is_expired(self) -> bool:
        """
        Verifica si la API Key ha expirado.
        """
        return datetime.now() > self.expiration_date

    def validate(self, raw_api_key: str) -> bool:
        """
        Valida si una API Key sin hash coincide con la clave almacenada.
        """
        if self.is_expired():
            return False  # La clave es inválida si ha expirado
        return manager.verify_password(raw_api_key, self.api_key_hashed)

    def renew(self, validity_period_days: int = 30) -> None:
        """
        Renueva la API Key actualizando su fecha de expiración.
        """
        self.expiration_date = datetime.now() + timedelta(days=validity_period_days)

    def activate_key(self):
        self.active = True

    def deactivate_key(self):
        self.active = False

    def __repr__(self):
        """
        Representación de la API Key (para debugging).
        """
        return (
            f"<ApiKey(created={self.create_date}, "
            f"expires={self.expiration_date}, "
            f"expired={self.is_expired()})>"
        )

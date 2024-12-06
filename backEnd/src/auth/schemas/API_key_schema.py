from pydantic import BaseModel, Field
from datetime import datetime
from ..models.API_key_model import ApiKeyModel

class ApiKeySchema(BaseModel):
    id: str = Field(..., description = "ID de la api key en la base de datos")
    api_key_hashed: str = Field(..., description = "La API key en formato hash")
    create_date: str = Field(..., description = "Fecha de creación de la api key")
    expiration_date: str = Field(..., description = "Fecha de expiracion de la api key")
    active : bool = Field(..., description = "Estado de la key, activo = True - desactivado = False")

    @classmethod
    def from_model(cls, model: ApiKeyModel, with_id: bool ) -> "ApiKeySchema":
       return cls(
           id = str(model.id) if with_id and model.id else None,
           api_key_hashed = model.api_key_hashed,
           create_date = str(model.create_date),
           expiration_date = str(model.expiration_date),
           active = model.active
       )
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),  # Convertir datetime a formato ISO 8601
        }
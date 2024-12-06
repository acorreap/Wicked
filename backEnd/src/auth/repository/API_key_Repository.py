import json
from typing import Optional, List
from datetime import datetime
from ..schemas.API_key_schema import ApiKeySchema
from ..models.API_key_model import ApiKeyModel
from pathlib import Path
from bson import ObjectId
from ...core.crypto import manager

class ApiKeyRepository:
    def __init__(self, db_path: str = "data/apikeys.json"):
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            # Si el archivo no existe, crea uno vacío
            self.db_path.write_text(json.dumps([]))

    def _read_db(self) -> List[dict]:
        """
        Lee el archivo JSON y retorna una lista de diccionarios.
        """
        with open(self.db_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _write_db(self, data: List[dict]):
        """
        Escribe datos en el archivo JSON.
        """
        with open(self.db_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def create(self, api_key: ApiKeySchema) -> ApiKeySchema:
        """
        Crea una nueva API Key en el archivo JSON.
        """
        data = self._read_db()
        api_key_dict = api_key.dict()
        data.append(api_key_dict)
        self._write_db(data)
        return api_key


    def get_by_id(self, api_key_id: str) -> Optional[ApiKeyModel]:
        data = self._read_db()
        for record in data:
            if record.get("_id") == api_key_id:  # Asegúrate de usar `_id`
                record["id"] = record["_id"]  # Mapea `_id` a `id`
                return ApiKeyModel(**record)
        return None

    def get_by_raw_key(self, raw_api_key: str) -> Optional[ApiKeyModel]:
        """
        Busca una API Key en la base de datos simulada utilizando la clave sin hashear.
        """
        data = self._read_db()

        for record in data:
            # Mapea el campo `id` a `_id` para que coincida con el modelo de MongoDB
            if "id" in record:
                record["_id"] = record.pop("id")

            # Valida si el raw_api_key coincide con el hash almacenado
            if manager.verify_data(raw_api_key, record.get("api_key_hashed", "")):
                return ApiKeyModel(**record)

        # Retorna None si no se encuentra la clave
        return None


    def get_all(self) -> List[ApiKeySchema]:
        """
        Retorna todas las API Keys.
        """
        data = self._read_db()
        return [ApiKeySchema(**record) for record in data]

    def update(self, api_key_id: str, updated_data: dict) -> Optional[ApiKeySchema]:
        """
        Actualiza una API Key por su ID.
        """
        data = self._read_db()
        for index, record in enumerate(data):
            if record["_id"] == api_key_id:
                data[index].update(updated_data)
                self._write_db(data)
                return ApiKeySchema(**data[index])
        return None

    def delete(self, api_key_id: str) -> bool:
        """
        Elimina una API Key por su ID.
        """
        data = self._read_db()
        new_data = [record for record in data if record["_id"] != api_key_id]
        if len(new_data) != len(data):
            self._write_db(new_data)
            return True
        return False

import json
from typing import Optional, List
from datetime import datetime
from ..schemas.API_key_schema import ApiKeySchema
from pathlib import Path


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

    def get_by_id(self, api_key_id: str) -> Optional[ApiKeySchema]:
        """
        Busca una API Key por su ID.
        """
        data = self._read_db()
        for record in data:
            if record["_id"] == api_key_id:
                return ApiKeySchema(**record)
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

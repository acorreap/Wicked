from ..repository.API_key_Repository import ApiKeyRepository
from ..models.API_key_model import ApiKeyModel
from ..schemas.API_key_schema import ApiKeySchema
from ...core.crypto import manager
class ApiKeyService():
    def __init__(self):
        self.api_key_repository = ApiKeyRepository()
        self.api_key_schema = ApiKeySchema

    def create_api_key(self, validaty_period_days = 90):
        api_key_model, raw_api_key = ApiKeyModel.generate(validaty_period_days)
        
        self.api_key_repository.create(self.api_key_schema.from_model(api_key_model, True))

        return {
            "api_key_raw": raw_api_key,
            "api_key_hashed": api_key_model.api_key_hashed,
            "expiration_date": api_key_model.expiration_date,
        }
    
    def valid_api_key(self, api_key_schema_id: str):
        api_key_model = self.api_key_repository.get_by_raw_key(api_key_schema_id)

        if not api_key_model:
            return False
        
        return True, str(api_key_model.api_key_hashed)

from fastapi import APIRouter, HTTPException, status
from ..service.API_key_service import ApiKeyService
from ..schemas.API_key_schema import ApiKeySchema
from fastapi.responses import JSONResponse

api_key_router = APIRouter()
api_service = ApiKeyService()


@api_key_router.post("/create")
def create_api_key():
    try:
        result = api_service.create_api_key()
        return {"message": "API Key creada exitosamente", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_key_router.get("/validate")
def validate_api_key(api_key: str):
    if api_service.validate_api_key(api_key):
        return {"message": "API Key válida"}
    else:
        raise HTTPException(status_code=401, detail="API Key inválida o expirada")

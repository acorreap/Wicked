from fastapi import APIRouter, Depends
from .auth.controller.AuthController import user_router
from .auth.controller.Api_Key_Controller import api_key_router


api_router = APIRouter()

api_router.include_router(user_router, prefix="/auth", tags=["auth"])
api_router.include_router(api_key_router, prefix="/apiKey", tags=["auth"])
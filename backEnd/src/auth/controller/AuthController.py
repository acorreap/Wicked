from fastapi import APIRouter


user_router = APIRouter()


@user_router.get("/user")
def get_user():
    return "probando api"
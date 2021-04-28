from fastapi import APIRouter
from .endpoints import login, users, infos, tradings


api_router = APIRouter()
api_router.include_router(login.router, tags=["login"], prefix='/login')
api_router.include_router(users.router, tags=["users"], prefix='/users')
from fastapi import APIRouter, Depends
from typing import Any
from fastapi.security import OAuth2PasswordBearer

from app import schemas
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post('/')
def login(user: schemas.User, token: str = Depends(oauth2_scheme)) -> Any:
    pass
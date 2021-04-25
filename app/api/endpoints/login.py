from fastapi import APIRouter
from typing import Any

from app import schemas
router = APIRouter()

@router.post('/')
def login(user: schemas.User) -> Any:
    pass
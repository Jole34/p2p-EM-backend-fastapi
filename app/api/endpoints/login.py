from fastapi import APIRouter
from typing import Any

import schemas

router = APIRouter()

@router.post('/')
def login(user: schemas.User) -> Any:
    pass
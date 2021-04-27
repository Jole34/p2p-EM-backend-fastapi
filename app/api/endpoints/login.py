from fastapi import APIRouter, Depends, HTTPException
from typing import Any
from db.session import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request

from app import schemas
from app import crud

import traceback
router = APIRouter()

@router.post('/login/')
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    pass

@router.post('/create-user/', response_model=schemas.ReturnMsg)
def create_user(user: schemas.User) -> Any:
        db = SessionLocal()
        if user.role > 3 or user.role == 0:
            raise HTTPException(
                status_code=400,
                detail="Invalid role"
            )       
        
        if len(user.hashed_password) < 8:
            raise HTTPException(
                status_code=400,
                detail="Short password"
            )               

        user = crud.user.create(db, obj_in=user)
        if not user:
            raise HTTPException(
                status_code=400,
                detail="Invalid data"
            )
        return {'msg':'User written in db.'}
        db.close()
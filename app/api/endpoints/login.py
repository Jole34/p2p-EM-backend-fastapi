from fastapi import APIRouter, Depends, HTTPException
from typing import Any
from app import db

from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request

from app import schemas
from app import crud
from db.session import SessionLocal
import traceback
import re
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
        
        if len(user.password) < 8:
            raise HTTPException(
                status_code=400,
                detail="Short password"
            )             

        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", user.email):
            raise HTTPException(
                status_code=400,
                detail="Not a valid email."
            )           

        user = crud.user.create(db, obj_in=user)
        if not user:
            raise HTTPException(
                status_code=400,
                detail="Invalid data"
            )
        return {'msg':'User written in db.'}
        db.close()
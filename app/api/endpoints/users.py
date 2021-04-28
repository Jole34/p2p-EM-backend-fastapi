from fastapi import APIRouter, Depends, HTTPException
from typing import Any
from app import db

from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request
from datetime import datetime, timedelta
import schemas
import crud
from db.session import SessionLocal
from settings.common import verify_token  
from models import User
import traceback
import re

router = APIRouter()

@router.get('/user-me/')
def get_user_me(user: User = Depends(verify_token)):
    return user;

@router.post('/create-user/', response_model=schemas.UserOutput)
def create_user(user: schemas.User) -> Any:
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
        db = SessionLocal()
        user = crud.user.create(db, obj_in=user)
        db.close()
        if not user:
            raise HTTPException(
                status_code=400,
                detail="Invalid data"
            )
        return user
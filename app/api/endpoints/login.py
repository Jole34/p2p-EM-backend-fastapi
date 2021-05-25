from fastapi import APIRouter, Depends, HTTPException
from typing import Any
from app import db

from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request
from datetime import datetime, timedelta
import schemas
import crud
from db.session import SessionLocal
from settings.common import create_token  

import traceback
import re
router = APIRouter()

@router.post('/login/')
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    db = SessionLocal()
    user_dict = crud.user.get_user(db, form_data.username, form_data.password)
    db.close()
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    secret = form_data.client_secret

    duration = timedelta(minutes=60*24*2)
    token = create_token(user_dict.id, expires=duration)
    user_dict_res = {
        "roles": [user_dict.role_id_1, user_dict.role_id_2, user_dict.role_id_3],
        "email": user_dict.email,
        "name": user_dict.name,
        "status": user_dict.status
    }
    return {"access_token": token, "token_type": "bearer", "user": user_dict_res}
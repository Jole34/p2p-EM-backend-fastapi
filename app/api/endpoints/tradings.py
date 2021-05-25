from fastapi import APIRouter, Depends, HTTPException
from typing import Any
from app import db
from fastapi_pagination import PaginationParams
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request
from datetime import datetime, timedelta
from db.session import SessionLocal
from settings.common import verify_token  
from models import User

import traceback
import re
import schemas
import crud

router = APIRouter()

@router.get('/get_all/')
def get_trading_me(user: User = Depends(verify_token), params: PaginationParams = Depends(), trading_type: str = None):
    if trading_type not in ['energy','money']:
        raise HTTPException(
                status_code=400,
                detail="Invalid data"
        )
    db = SessionLocal()
    query = crud.trade.get_trades_by_user(db, user.id, trading_type)
    db.close()
    trades = paginate(query, params)
    return trades
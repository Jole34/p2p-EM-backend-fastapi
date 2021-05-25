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

@router.post('/buy/')
def buy_energy(user: User = Depends(verify_token), energy_amount: float = None, money_amount: float = None):
   
    if not energy_amount and not money_amount:
        raise HTTPException(
                status_code=400,
                detail="Invalid data"
        )   
    if energy_amount:   
        db = SessionLocal()
        balance = crud.billing.get_balance_by_user_id(db, user.id)
        amount = balance.money_amount
        if energy_amount*4.2 > amount:
                raise HTTPException(
                status_code=400,
                detail="Not enough money."
        )      
        balance.money_amount = balance.money_amount-energy_amount*4.2
        crud.billing.update(db, balance)
        
    else:
        balance.money_amount = balance.money_amount-money_amount
        if balance.money_amount < money_amount:
                raise HTTPException(
                status_code=400,
                detail="Not enough money."
        )              
        balance.energy_amount = balance.energy_amount+(money_amount*4.2)
        crud.billing.update(db, balance)

    db.close()
    return balance.money_amount

@router.post('/sell/')
def sell_energy(user: User = Depends(verify_token), energy_amount: float):
    if not energy_amount:
        raise HTTPException(
                status_code=400,
                detail="Invalid data"
        )   
    db = SessionLocal()
    balance = crud.billing.get_balance_by_user_id(db, user.id)
    amount = balance.energy_amount
    if energy_amount < amount:
            raise HTTPException(
            status_code=400,
            detail="Not enough energy to sell."
    )      
    balance.energy_amount = balance.energy_amount-energy_amount
    crud.billing.update(db, balance)
    db.close()
    return balance.energy_amount


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


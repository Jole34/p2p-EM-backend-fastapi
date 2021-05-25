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
import requests 

router = APIRouter()

@router.post('/buy/')
def buy_energy(user: User = Depends(verify_token), energy_amount: float = None, money_amount: float = None):
    if not energy_amount and not money_amount:
        raise HTTPException(
                status_code=400,
                detail="Invalid data"
        )   
    db = SessionLocal()
    try:
        constant = requests.get('https://api.coinbase.com/v2/prices/spot?currency=USD').json()
        result_constant = float(constant['data']['amount'])/1000
    except:
        raise HTTPException(
                status_code=400,
                detail="Invalid data"
        )  
    if energy_amount:   
        balance = crud.billing.get_balance_by_user_id(db, user.id)
        if not balance:
            raise HTTPException(
                    status_code=400,
                    detail="Invalid data"
            )   
        amount = balance.money_amount
        if energy_amount*result_constant > amount:
                raise HTTPException(
                status_code=400,
                detail="Not enough money."
        )      
        balance.money_amount = balance.money_amount-energy_amount*result_constant
        balance.energy_amount = balance.energy_amount+energy_amount
        crud.billing.update(db, balance)
        
    else:
        balance = crud.billing.get_balance_by_user_id(db, user.id)
        if not balance:
            raise HTTPException(
                    status_code=400,
                    detail="Invalid data"
            )   
        if balance.money_amount-money_amount < money_amount:
                raise HTTPException(
                status_code=400,
                detail="Not enough money."
        )              
        balance.energy_amount = int(balance.energy_amount+(money_amount/result_constant)*100)/100
        balance.money_amount = balance.money_amount-money_amount
        crud.billing.update(db, balance)

    db.close()
    return "Success"

@router.post('/sell/')
def sell_energy(user: User = Depends(verify_token), energy_amount: float = None):
    if not energy_amount:
        raise HTTPException(
                status_code=400,
                detail="Invalid data"
        )   
    db = SessionLocal()
    try:
        constant = requests.get('https://api.coinbase.com/v2/prices/spot?currency=USD').json()
        result_constant = float(constant['data']['amount'])/1000
    except:
        raise HTTPException(
                status_code=400,
                detail="Invalid data"
        )  
    balance = crud.billing.get_balance_by_user_id(db, user.id)
    if not balance:
        raise HTTPException(
                status_code=400,
                detail="Invalid data"
        )   
    amount = balance.energy_amount
    if energy_amount > amount:
            raise HTTPException(
            status_code=400,
            detail="Not enough energy to sell."
    )      
    balance.energy_amount = balance.energy_amount-energy_amount
    balance.money_amount = balance.money_amount-energy_amount*result_constant
    crud.billing.update(db, balance)
    db.close()
    return "Success"


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


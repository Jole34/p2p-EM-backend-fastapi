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
import models
import crud
import requests 
import uuid

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
        result_constant = int(float(constant['data']['amount'])/10000*100)/100
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
        trade = models.Trade(
            description='Buy from energy',
            action='buy',
            trade_type='energy',
            amount=energy_amount,
            price=(1/result_constant),
            moment_balance=balance.energy_amount,
            trade_id=str(uuid.uuid1()),
            currency='USD',
            user_id=user.id
        )
        crud.trade.create(db, trade)
    else:
        balance = crud.billing.get_balance_by_user_id(db, user.id)
        if not balance:
            raise HTTPException(
                    status_code=400,
                    detail="Invalid data"
            )   
        if balance.money_amount-money_amount < 0:
                raise HTTPException(
                status_code=400,
                detail="Not enough money."
        )              
        balance.energy_amount = balance.energy_amount+(money_amount/result_constant)
        balance.money_amount = balance.money_amount -money_amount
        crud.billing.update(db, balance)
        trade = models.Trade(
            description='Buy from money',
            action='buy',
            trade_type='money',
            amount=money_amount,
            price=result_constant,
            moment_balance=balance.energy_amount,
            trade_id=str(uuid.uuid1()),
            currency='USD',
            user_id=user.id
        )
        crud.trade.create(db, trade)
    balance = crud.billing.get_balance_by_user_id(db, user.id)
    db.close()
    return {"energy": balance.energy_amount, "money": balance.money_amount, "rate": result_constant}

@router.post('/sell/')
def sell_energy(user: User = Depends(verify_token), energy_amount: schemas.Energy = None):
    print(energy_amount.energy_amount)
    if not energy_amount.energy_amount:
        raise HTTPException(
                status_code=400,
                detail="Invalid data, amount is none"
        )   
    db = SessionLocal()
    try:
        constant = requests.get('https://api.coinbase.com/v2/prices/spot?currency=USD').json()
        result_constant = int(float(constant['data']['amount'])/10000*100)/100
    except:
        raise HTTPException(
                status_code=400,
                detail="Invalid data, api for currency failed"
        )  
    balance = crud.billing.get_balance_by_user_id(db, user.id)
    if not balance:
        raise HTTPException(
                status_code=400,
                detail="Invalid data, there is no billing for user"
        )   
    amount = balance.energy_amount
    if energy_amount.energy_amount > amount:
        raise HTTPException(
            status_code=400,
            detail="Not enough energy to sell."
    )      
    balance.energy_amount = balance.energy_amount-energy_amount.energy_amount
    balance.money_amount = balance.money_amount+energy_amount.energy_amount*result_constant
    crud.billing.update(db, balance)
    trade = models.Trade(
            description='Sell from energy',
            action='sell',
            trade_type='energy',
            amount=energy_amount.energy_amount,
            price=1/result_constant,
            moment_balance=balance.energy_amount,
            trade_id=str(uuid.uuid1()),
            currency='USD',
            user_id=user.id
        )
        
    crud.trade.create(db, trade)
    balance = crud.billing.get_balance_by_user_id(db, user.id)
    db.close()
    return {"energy": balance.energy_amount, "money": balance.money_amount, "rate": result_constant}

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


@router.get('/get_rate/')
def get_rate():
    try:
        constant = requests.get('https://api.coinbase.com/v2/prices/spot?currency=USD').json()
        result_constant = int(float(constant['data']['amount'])/10000*100)/100
    except:
        raise HTTPException(
                status_code=400,
                detail="Invalid data"
        )  
    return result_constant
from jose import jwt
from pydantic import ValidationError
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from db.session import SessionLocal

import crud

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/p2p/login/login/"
)

def create_token(email, expires):
    if expires:
        expire = datetime.utcnow() + expires
    else:
        expire = datetime.utcnow() + timedelta(
            minutes= 60 * 24 *2
        )
    to_encode = {"exp": expire, "sub": str(email)}
    encoded_jwt = jwt.encode(to_encode,'dbc7b90ac76a4b8c9f4f67551b66712906288c756f2b47e49d8c42e597dc27bd' , algorithm='HS256')
    return encoded_jwt

def verify_token(token: str = Depends(reusable_oauth2)):
    db = SessionLocal()
    try:
        payload = jwt.decode(
            token, 'dbc7b90ac76a4b8c9f4f67551b66712906288c756f2b47e49d8c42e597dc27bd', algorithms='HS256'
        )
        token_data = payload
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get_user_by_id(db, token_data['sub'])
    db.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
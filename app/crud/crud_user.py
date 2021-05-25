import traceback
from typing import Any, Dict, Optional, Union, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime

import os
import hashlib
import hmac
import models
import schemas

class CRUDUser():
    def create(self, db: Session, obj_in: schemas.User) -> Optional[models.User]:
        salt = 'str'.encode("ascii")
        pw_hash = hashlib.pbkdf2_hmac('sha256', obj_in.password.encode(), salt, 100000)
        db_obj = models.User(
            name=obj_in.name,
            last_name=obj_in.last_name,
            email=obj_in.email,
            hashed_password=str(pw_hash),
            role_id=obj_in.role_id
        )
        db.add(db_obj)
        try:
            db.commit()
        except SQLAlchemyError:
            traceback.print_exc()
            return None
        db.refresh(db_obj)
        return db_obj

    def get_user(self, db: Session, email: str, password: str) ->  Optional[models.User]:
        salt = 'str'.encode("ascii")
        password = str(hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000))
        return db.query(models.User).filter(models.User.email == email, models.User.hashed_password == password).first()
    
    def get_user_email(self, db: Session, email: str) -> Optional[models.User]:
        return db.query(models.User).filter(models.User.email == email).first()     

    def get_user_by_id(self, db: Session, id: int) -> Optional[models.User]:
        return db.query(models.User).filter(models.User.id == id).first() 
            
user = CRUDUser()


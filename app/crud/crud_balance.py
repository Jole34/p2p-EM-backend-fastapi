import traceback
from typing import Any, Dict, Optional, Union, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime

import models
import schemas
class CRUDBalance():
    def create(self, db: Session, obj_in: schemas.Balance) -> Optional[models.Balance]:
            db_obj = models.Balance(
                ammount=obj_in.ammount,
                user_id=obj_in.user_id
            )
            db.add(db_obj)
            try:
                db.commit()
            except SQLAlchemyError:
                traceback.print_exc()
                return None
            db.refresh(db_obj)
            return db_obj

    def get_balance_by_id(self, db: Session, id: int) -> Optional[models.Balance]:
        return db.query(models.Balance).filter(models.Balance.id == id).first()  

    def get_balance_by_user_id(self, db: Session, id: int) -> Optional[models.Balance]:
        return db.query(models.Balance).filter(models.Balance.user_id == id).first()  


balance = CRUDBalance()
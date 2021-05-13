import traceback
from typing import Any, Dict, Optional, Union, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime

import models
import schemas
class CRUDBilling():
    def create(self, db: Session, obj_in: schemas.Billing) -> Optional[models.Billing]:
            db_obj = models.Billing(
                name=obj_in.name,
                last_name=obj_in.last_name,
                email=obj_in.email,
                hashed_password=obj_in.password,
                role_id=obj_in.role
            )
            db.add(db_obj)
            try:
                db.commit()
            except SQLAlchemyError:
                traceback.print_exc()
                return None
            db.refresh(db_obj)
            return db_obj


    def get_billing_by_user_id(self, db: Session, id: int) -> Optional[models.Billing]:
        return db.query(models.Billing).filter(models.Billing.user_id == id).first()  

    def get_balance_by_user_id(self, db: Session, id: int) -> Optional[models.Billing]: 
        return db.query(models.Billing).filter(models.Billing.user_id == id).first()  

billing = CRUDBilling()
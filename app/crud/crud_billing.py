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
                addres=obj_in.address_line,
                city=obj_in.city,
                country=obj_in.country,
                zip_code=obj_in.zip_code,
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

    def update(self, db: Session, obj_in: dict, **kwargs) -> bool:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        db_obj = db.query(models.Billing).filter(models.Billing.id == kwargs['id']).first()
        if not db_obj:
            return False
        super().update(db, db_obj=db_obj, obj_in=update_data)
        return True

    def get_billing_by_user_id(self, db: Session, id: int) -> Optional[models.Billing]:
        return db.query(models.Billing).filter(models.Billing.user_id == id).first()  

    def get_balance_by_user_id(self, db: Session, id: int) -> Optional[models.Billing]: 
        return db.query(models.Billing).filter(models.Billing.user_id == id).first()  

billing = CRUDBilling()
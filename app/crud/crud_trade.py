from typing import Any, Dict, Optional, Union, List
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime

import traceback
import models
import schemas
class CRUDTrade():
    def create(self, db: Session, obj_in: models.Trade) -> Optional[models.Trade]:
            db.add(obj_in)
            try:
                db.commit()
            except SQLAlchemyError:
                traceback.print_exc()
                return None
            db.refresh(obj_in)
            return obj_in

    def get_trades_by_user(self, db: Session, user_id: int, trading_type: str) -> Optional[models.Trade]:
        return db.query(models.Trade).filter(models.Trade.user_id == user_id, models.Trade.trade_type == trading_type).order_by(models.Trade.created_on.desc())

    def get_all_trades(self, db: Session):
        return db.query(models.Trade)

    def get_blockchain_trade(self, db: Session, trade_id: int) -> Optional[models.BlockchainTrade]:
        return db.query(models.BlockchainTrade).filter(models.BlockchainTrade.trade_id == trade_id).first()

trade = CRUDTrade()
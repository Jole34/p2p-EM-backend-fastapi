from typing import Any, Dict, Optional, Union, List
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime

import traceback
import models
import schemas
class CRUDTrade():
    def get_trades_by_user(self, db: Session, user_id: int, trading_type: str) -> Optional[models.Trade]:
        return db.query(models.Trade).filter(models.Trade.user_id == user_id, models.Trade.trade_type == trading_type)


trade = CRUDTrade()
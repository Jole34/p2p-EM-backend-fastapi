from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Energy(BaseModel):
    energy_amount: float

class Trade(BaseModel):
    created_on: datetime
    action: str
    trade_type: str
    amount: Optional[float] =  None
    user_id: int
    
    class Config:
        orm_mode = True


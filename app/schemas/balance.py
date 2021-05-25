from pydantic import BaseModel, EmailStr
from typing import Optional

class Balance(BaseModel):
    money_amount: float

class BalanceEnergy(BaseModel):
    energy_amount: float

class BalanceCreate(BaseModel):
    money_amount: Optional[float] = 0
    energy_amount: Optional[float] = 0
    user_id: int

    class Config:
        orm_mode = True
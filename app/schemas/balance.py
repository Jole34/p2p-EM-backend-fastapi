from pydantic import BaseModel, EmailStr

class Balance(BaseModel):
    ammount: float


class BalanceCreate(BaseModel):
    ammount: float
    user_id: int

    class Config:
        orm_mode = True
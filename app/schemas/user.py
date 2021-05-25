from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    password: str
    role_id: int

class UserOutput(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    role_id: int

    class Config:
        orm_mode = True
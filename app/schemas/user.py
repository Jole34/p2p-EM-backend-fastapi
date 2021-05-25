from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    password: str
    role_id_1: Optional[int] = None
    role_id_2: Optional[int] = None
    role_id_3: Optional[int] = None

class UserOutput(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    role_id_1: Optional[int] = None
    role_id_2: Optional[int] = None
    role_id_3: Optional[int] = None

    class Config:
        orm_mode = True
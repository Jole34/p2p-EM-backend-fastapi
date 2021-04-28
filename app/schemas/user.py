from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    password: str
    role: int

class UserOutput(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    role_id: int
    
    class Config:
        orm_mode = True
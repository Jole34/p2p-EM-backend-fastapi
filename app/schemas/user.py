from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    password: str
    role: int
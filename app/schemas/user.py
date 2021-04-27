from pydantic import BaseModel

class User(BaseModel):
    name: str
    last_name: str
    email: str
    hashed_password: str
    role: int

    class Config:
        orm_mode = True
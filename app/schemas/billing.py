from pydantic import BaseModel, EmailStr

class Billing(BaseModel):
    address_line: str
    city: str
    country: str
    zip_code: str
    balance_id: int

class BillingIn(BaseModel):
    address_line: str
    city: str
    country: str
    zip_code: str
    balance_id: int
    user_id: int
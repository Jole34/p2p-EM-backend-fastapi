from pydantic import BaseModel, EmailStr

class Billing(BaseModel):
    address_line: str
    city: str
    country: str
    zip_code: str

class BillingIn(BaseModel):
    address_line: str
    city: str
    country: str
    zip_code: str
    user_id: int
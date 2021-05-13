from pydantic import BaseModel, EmailStr
from typing import Optional

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

class BillingUpdate(BaseModel):
    address_line: Optional[str] = None 
    city: Optional[str] = None 
    country: Optional[str] = None 
    zip_code: Optional[str] = None 
    discount: Optional[float] = None 
    amount: Optional[float] = None
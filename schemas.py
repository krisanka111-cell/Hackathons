from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    city: str
    income: float
    purpose: str

class UserOut(BaseModel):
    user_id: int
    name: str
    city: str
    income: float
    purpose: str

class SchemeOut(BaseModel):
    scheme_id: int
    scheme_name: str
    category: str
    interest_rate: float

class PartnerOut(BaseModel):
    partner_id: int
    partner_name: str
    location: str

class ApplicationCreate(BaseModel):
    user_id: int
    scheme_id: int
    partner_id: int
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict


class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(
        ..., min_length=6, description="Password must be at least 6 characters"
    )


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6)
    recent_order: Optional[str] = None
    my_plants: Optional[Dict] = None


class UserResponse(UserBase):
    id: int
    recent_order: Optional[str] = None
    my_plants: Optional[Dict] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None

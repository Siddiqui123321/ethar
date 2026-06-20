from pydantic import BaseModel, Field, EmailStr, conint
from typing import List, Optional

class ProductBase(BaseModel):
    name: str = Field(...)
    sku: str = Field(...)
    price: float = Field(..., ge=0)
    quantity: int = Field(..., ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]
    quantity: Optional[int]

class ProductRead(ProductBase):
    id: int

    class Config:
        orm_mode = True

class CustomerBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str]

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: int

    class Config:
        orm_mode = True

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: conint(gt=0)

class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemCreate]

class OrderItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float

    class Config:
        orm_mode = True

class OrderRead(BaseModel):
    id: int
    customer_id: int
    total_amount: float
    items: List[OrderItemRead]

    class Config:
        orm_mode = True

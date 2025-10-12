from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Customer Schemas
class CustomerBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# OrderItem Schemas
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int
    price_at_time: float

    class Config:
        from_attributes = True


# Order Schemas
class OrderBase(BaseModel):
    customer_id: int
    status: str = "pending"


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class Order(OrderBase):
    id: int
    order_date: datetime
    total_amount: float
    items: List[OrderItem] = []

    class Config:
        from_attributes = True


# Response Models
class CustomerWithOrders(Customer):
    orders: List[Order] = []


class OrderWithDetails(Order):
    customer: Customer
    items: List[OrderItem] = []

from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    price_without_discount: float
    discount_percent: int
    in_stock: bool = True
    quantity: int

class OrderCreated(BaseModel):
    orderid:str = uuid.uuid1()
    username:str
    useremail:EmailStr
    phonenumber:str
    address:str
    payment:str = "Cash On Delivery"
    deliverystatus:str = "Pending"
    product_details:list
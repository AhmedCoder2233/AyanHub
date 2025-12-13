from pydantic import BaseModel
import random

ID = random.randint(500, 1000) * 4

class AllProducts(BaseModel):
    product_name:str
    product_description:str
    product_price:str
    product_category:str
    
class OrderedUser(BaseModel):
    orderid:int = ID
    email:str
    phone:str
    address:str 
    orderstatus:str = "Pending"
    isconfirmed:bool = False
    product:list

class OrderStatusRequest(BaseModel):
    orderid: int
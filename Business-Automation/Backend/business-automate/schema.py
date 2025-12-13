from pydantic import BaseModel

class AllProducts(BaseModel):
    name:str
    description:str
    price:int 
    image_url:str
    quantity:int
    sent_alert:bool

class PurchaseUser(BaseModel):
    order_id:str
    name:str
    email:str
    phone:str
    address:str
    payment_method:str
    status:str
    product_name:str
    product_description:str
    product_price:int
    product_quantity:int
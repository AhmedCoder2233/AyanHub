from sqlalchemy import Column, String, Integer, Float, Boolean, JSON
from database import Base

class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    price_without_discount = Column(Float, nullable=False)
    discount_percent = Column(Integer, nullable=False)
    in_stock = Column(Boolean, default=True)
    quantity = Column(Integer, nullable=False)

class OrderCreate(Base):
    __tablename__ = "ordercreate"
    id = Column(Integer, primary_key=True, index=True)
    orderid = Column(String, nullable=False)
    username = Column(String, nullable=False)
    useremail = Column(String , nullable=False)
    phonenumber = Column(String , nullable=False)
    address = Column(String, nullable=False)
    payment = Column(String, nullable=False, default="Cash On Delivery")
    deliverystatus = Column(String, nullable=False, default="Pending")
    product_details = Column(JSON, nullable=False)

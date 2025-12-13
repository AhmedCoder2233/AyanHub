from database import Base
from sqlalchemy import Column, String, Integer, Boolean, JSON

class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    product_description = Column(String, nullable=False)
    product_price = Column(String, nullable=False)
    product_category = Column(String, nullable=False)

class PlaceOrder(Base):
    __tablename__ = "placeorder"
    id = Column(Integer, primary_key=True, index=True)
    orderid = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    orderstatus = Column(String, nullable=False)
    isconfirmed = Column(Boolean, nullable=False)
    product = Column(JSON, nullable=False)

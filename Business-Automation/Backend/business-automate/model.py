from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    image_url = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    sent_alert = Column(Boolean, nullable=False)

class UserInfo(Base):
    __tablename__ = "userinfo"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    payment_method = Column(String, nullable=False)
    status = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    product_description = Column(String, nullable=False)
    product_price = Column(Integer, nullable=False)
    product_quantity = Column(Integer, nullable=False)
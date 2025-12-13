from database import Base
from sqlalchemy import Column, String, Integer, JSON

class OrderTable(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    useremail = Column(String, nullable=False)
    fooditem = Column(String, nullable=False)

class Menu(Base):
    __tablename__ = "menu"
    id = Column(Integer, primary_key=True)
    dishes = Column(String, nullable=False)
    dishes_price = Column(String, nullable=False)
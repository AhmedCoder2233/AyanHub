from fastapi import FastAPI, Depends
from database import engine, LocalSession
from sqlalchemy.orm import Session
from model import Products, OrderCreate
from schema import ProductBase, OrderCreated
from model import Base
from twilio.rest import Client
import os

Base.metadata.create_all(bind=engine)

app = FastAPI()

Account_Sid = os.getenv("ACCOUNT_SID")
Auth_Token = os.getenv("AUTH_TOKEN")
client = Client(Account_Sid, Auth_Token)

def getdb():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

@app.post("/product")
def ProductPost(product:ProductBase ,db:Session = Depends(getdb)):
    addPro = Products(**product.model_dump())
    db.add(addPro)
    db.commit()
    return "Succesfully Data Posted"

@app.get("/productquantity")
def getProduct(db: Session = Depends(getdb)):
    data = db.query(Products).filter(Products.quantity <= 3).all()
    
    if data:
        for item in data:
            client.messages.create(
                from_='whatsapp:+14155238886',
                body=f"This Product {item.name} with description {item.description} with price {item.price} has just {item.quantity} pieces Left 👀",
                to='whatsapp:+923368952826'
            )
            client.calls.create(
            from_='+14633070897',
            to='+923368952826',
            url='http://demo.twilio.com/docs/voice.xml'
        )
        return data
    
    return "No Data Found That is below than 3"

@app.get("/totalproducts")
def getProducts(db:Session = Depends(getdb)):
    return db.query(Products).all()

@app.post("/ordercreate")
def OrderPlaced(data:OrderCreated ,db:Session = Depends(getdb)):
    userorder = OrderCreate(**data.model_dump())
    db.add(userorder)
    db.commit()
    return "User Order Placed!"
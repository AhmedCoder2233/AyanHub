import model
from model import Base, Products, UserInfo
from database import engine, LocalSession
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from schema import AllProducts, PurchaseUser
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)


def getdb():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

@app.post("/product/")
def post_products(products:AllProducts ,db: Session = Depends(getdb)):
    data = Products(**products.model_dump())
    db.add(data)
    db.commit()
    return {"message": "All products inserted successfully!"}

@app.get("/product/")
def get_products(db:Session = Depends(getdb)):
    return db.query(Products).all()

@app.get("/low-stock-check/")
def check_low_stock(db: Session = Depends(getdb)):
    low_stock_products = db.query(Products).filter(Products.quantity <= 2).all()

    if low_stock_products:
        product_names = [p.name for p in low_stock_products]
        return {
            "error": "Some products have low stock (≤ 2)",
            "products": product_names
        }
    return {"message": "All products have sufficient stock"}


@app.post("/quantity-decrease/{product_name}")
def quantity_decrease(product_name: str, db: Session = Depends(getdb)):
    product = db.query(Products).filter(Products.name == product_name).first()

    if not product:
        return {"error": "Product not found"}
    if product.quantity <= 0:
        return {"error": "Out of stock"}
    product.quantity -= 1
    db.commit()

    return {"message": f"Quantity decreased. {product.quantity} remaining."}

@app.post("/userinfo/")
def UserInfoPost(info:PurchaseUser ,db:Session = Depends(getdb)):
    user = UserInfo(**info.model_dump())
    db.add(user)
    db.commit()
    return "UserInfo Posted"

@app.get("/userinfo/")
def getUserInfo(db:Session = Depends(getdb)):
    return db.query(UserInfo).all()

@app.post("/sent_alert_done/{product_name}")
def sentAlert(product_name:str, db:Session = Depends(getdb)):
    data = db.query(Products).filter(Products.name == product_name).first()
    if not data:
        return "Product Not Found"
    data.sent_alert = True
    db.commit()
    return "Sent Alert Succesfully"

from pydantic import BaseModel

class StatusChangeSchema(BaseModel):
    order_id: str
    status: str

@app.post("/statuschange/")
def ChangingStatus(data: StatusChangeSchema, db: Session = Depends(getdb)):
    order = db.query(UserInfo).filter(UserInfo.order_id == data.order_id).first()
    if not order:
        return {"error": "No OrderId matching..."}
    order.status = data.status
    db.commit()
    return {"message": "Successfully changed status"}
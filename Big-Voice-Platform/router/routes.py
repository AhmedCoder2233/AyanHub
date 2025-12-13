from fastapi import APIRouter, Depends, Request, BackgroundTasks
from apscheduler.schedulers.background import BackgroundScheduler
from model import Products, Base, PlaceOrder
from database import engine, LocalSession
from sqlalchemy import and_
from sqlalchemy.orm import Session
from schema import AllProducts, OrderedUser, OrderStatusRequest
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

Base.metadata.create_all(bind=engine)

load_dotenv()

router = APIRouter()

scheduler = BackgroundScheduler()

def getdb():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

def send_Email(to:str, subject:str, body:str):
    message = EmailMessage()
    message["to"] = to
    message["from"] = "ahmedmemon3344@gmail.com"
    message["subject"] = subject
    message.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("ahmedmemon3344@gmail.com", os.getenv("APP_PASS"))
        server.send_message(message)

def cancel_book_if_not_payment(order_id:str):
    db = getdb()
    checking = db.query(PlaceOrder)(and_(
        PlaceOrder.orderid == order_id,
        PlaceOrder.isconfirmed == False
    )).first()
    if checking:
        db.delete(checking)
        db.commit()
        print("User Deleted Succesfully!")

@router.post("/product")
def postProducts(Product:AllProducts,db:Session = Depends(getdb)):
    data = Products(**Product.model_dump())
    db.add(data)
    db.commit()
    return "Product Saved Succesfully"

@router.get("/products")
def getProducts(db:Session = Depends(getdb)):
    return db.query(Products).all()

@router.post("/orderplace")
def placeOrder(order:OrderedUser , background_task:BackgroundTasks, db:Session = Depends(getdb)):
    data = PlaceOrder(**order.model_dump())
    db.add(data)
    db.commit()
    scheduler.add_job(cancel_book_if_not_payment, trigger='date',
            run_date=datetime.now() + timedelta(minutes=30), args=[data.orderid])
    
    background_task.add_task(send_Email, order.email, "Your Order ID & Confirm Your Payment!", f"Thank you for your order! your order id is: {order.orderid} please confirm the payment from the link provided on Website to confirm your order Otherwise your order get cancelled within 10 Minutes!")

    return {"orderid": order.orderid}

@router.get("/orderstatus/{orderid}")
def getOrderStatus(orderid:int, db:Session = Depends(getdb)):
    data = db.query(PlaceOrder).filter(PlaceOrder.orderid == orderid).first()
    if not data:  
        return {"message": "Order Not Found!", "status": "failed"}
    return {"message": f"Your Order Status is {data.orderstatus}", "status": "success", "orderstatus": data.orderstatus}

@router.get("/orderstatusdata/{orderid}")
def getOrderData(orderid:int, db:Session = Depends(getdb)):
    data = db.query(PlaceOrder).filter(PlaceOrder.orderid == orderid).first()
    return data

@router.post("/webhook")
async def stripe_webhook(request: Request,background_task:BackgroundTasks ,db: Session = Depends(getdb)):
    payload = await request.json()
    event = payload  

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        email = session['metadata'].get('email')
        print(f"✅ Payment succeeded for email: {email}")

        if email:
            booking = db.query(PlaceOrder).filter(
                and_(
                PlaceOrder.email == email,
                PlaceOrder.isconfirmed == False
            )
            ).first()

            if booking:
                booking.isconfirmed = True
                db.commit()
                print("✅ Booking confirmed for:", email)

                background_task.add_task(send_Email, email, "Your Order ID & Confirm Your Payment!", "Your Order has been confirmed! use your Order ID on our website to check your delivery status!")

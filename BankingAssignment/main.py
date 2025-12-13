from fastapi import FastAPI, HTTPException
from model import AuthRequest, Transaction, Transfer
from utils import load_data, save_data

app = FastAPI()

# -------- AUTH --------
@app.post("/auth")
def authenticate(body: AuthRequest):
    data = load_data()
    for user in data["users"]:
        if user["username"] == body.username and user["pin"] == body.pin:
            return {"message": "User Already Exist", "user": user["username"]}
    data["users"].append({
        "username": body.username,
        "pin": body.pin,
        "balance": 0
    })
    save_data(data)
    return {"message": "User Created Succesfully"}


# -------- BALANCE --------
@app.get("/balance/{username}")
def get_balance(username: str):
    data = load_data()
    for user in data["users"]:
        if user["username"] == username:
            return {"balance": user["balance"]}
    raise HTTPException(status_code=404, detail="User not found")


# -------- DEPOSIT --------
@app.post("/deposit/{username}")
def deposit(username: str, body: Transaction):
    data = load_data()
    for user in data["users"]:
        if user["username"] == username:
            user["balance"] += body.amount
            save_data(data)
            return {"message": "Deposit successful", "new_balance": user["balance"]}
    raise HTTPException(status_code=404, detail="User not found")


# -------- WITHDRAW --------
@app.post("/withdraw/{username}")
def withdraw(username: str, body: Transaction):
    data = load_data()
    for user in data["users"]:
        if user["username"] == username:
            if user["balance"] < body.amount:
                raise HTTPException(status_code=400, detail="Insufficient funds")
            user["balance"] -= body.amount
            save_data(data)
            return {"message": "Withdraw successful", "new_balance": user["balance"]}
    raise HTTPException(status_code=404, detail="User not found")


# -------- TRANSFER --------
@app.post("/transfer/{username}")
def transfer(username: str, body: Transfer):
    data = load_data()
    from_user = None
    to_user = None

    for user in data["users"]:
        if user["username"] == username:
            from_user = user
        if user["username"] == body.to_user:
            to_user = user

    if not from_user or not to_user:
        raise HTTPException(status_code=404, detail="User not found")

    if from_user["balance"] < body.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    from_user["balance"] -= body.amount
    to_user["balance"] += body.amount

    save_data(data)
    return {"message": "Transfer success", "from_balance": from_user["balance"]}

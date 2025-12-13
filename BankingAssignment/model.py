from pydantic import BaseModel

class AuthRequest(BaseModel):
    username: str
    pin: str

class Transaction(BaseModel):
    amount: int

class Transfer(BaseModel):
    to_user: str
    amount: int

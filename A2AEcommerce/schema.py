from pydantic import BaseModel

class Orderdata(BaseModel):
    username:str
    useremail:str
    fooditem:str
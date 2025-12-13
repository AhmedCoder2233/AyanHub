from fastmcp import FastMCP
from model import Base, OrderTable, Menu
from database import engine, LocalSession
from schema import Orderdata

Base.metadata.create_all(bind=engine)

mcp = FastMCP(name="OrderServer", stateless_http=True)

@mcp.tool()
def placeOrder(orderdata:Orderdata):
    db = LocalSession()
    data = OrderTable(**orderdata.model_dump())
    db.add(data)
    db.commit()
    db.close()
    return "Order Placed Succesfully"

@mcp.tool()
def getMenu():
    db = LocalSession()
    query = db.query(Menu).all()
    result = [
        {
            "name": item.dishes,
            "price": item.dishes_price
        }
        for item in query
    ]
    db.close()
    return result
mcprun = mcp.streamable_http_app()
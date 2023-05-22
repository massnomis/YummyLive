from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
import uuid
import uvicorn
from time import time
app = FastAPI()

security = HTTPBasic()

class OrderType(str, Enum):
    buy = "buy"
    sell = "sell"

class Order(BaseModel):
    id: str
    type: OrderType
    price: Optional[float]
    quantity: float
    # add timestamp

order_book = {
    "buy": [],
    "sell": []
}
class User(BaseModel):
    username: str
    password: str

users = {
    "alice": User(username="alice", password="password"),
    "bob": User(username="bob", password="password"),
    "charlie": User(username="charlie", password="password")
}

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = users.get(credentials.username)
    if not user or not secrets.compare_digest(user.password, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user

@app.post("/order/", dependencies=[Depends(authenticate_user)])
async def create_order(order: Order):
    if order.price is None:
        # This is a market order
        if order.type == "buy":
            while order.quantity > 0 and order_book["sell"]:
                sell_order = order_book["sell"][0]
                if sell_order.quantity > order.quantity:
                    sell_order.quantity -= order.quantity
                    order.quantity = 0
                else:
                    order.quantity -= sell_order.quantity
                    order_book["sell"].pop(0)
        else:  # order.type == "sell"
            while order.quantity > 0 and order_book["buy"]:
                buy_order = order_book["buy"][0]
                if buy_order.quantity > order.quantity:
                    buy_order.quantity -= order.quantity
                    order.quantity = 0
                else:
                    order.quantity -= buy_order.quantity
                    order_book["buy"].pop(0)
    else:
        # This is a limit order
        order_book[order.type].append(order)
        order_book[order.type] = sorted(order_book[order.type], key=lambda x: x.price, reverse=(order.type == "buy"))
        match_orders()
    return {"message": "Order added"}

@app.delete("/order/{order_id}")
async def delete_order(order_id: str):
    for order_type in ["buy", "sell"]:
        for order in order_book[order_type]:
            if order.id == order_id:
                order_book[order_type].remove(order)
                return {"message": "Order deleted"}
    raise HTTPException(status_code=404, detail="Order not found")

@app.put("/order/{order_id}")
async def update_order(order_id: str, order: Order):
    for order_type in ["buy", "sell"]:
        for index, existing_order in enumerate(order_book[order_type]):
            if existing_order.id == order_id:
                order_book[order_type][index] = order
                order_book[order_type] = sorted(order_book[order_type], key=lambda x: x.price, reverse=(order.type == "buy"))
                match_orders()
                return {"message": "Order updated"}
    raise HTTPException(status_code=404, detail="Order not found")

order_history = []

def match_orders():
    global order_history
    while order_book["buy"] and order_book["sell"] and order_book["buy"][0].price >= order_book["sell"][0].price:
        buy_order = order_book["buy"][0]
        sell_order = order_book["sell"][0]
        if buy_order.quantity > sell_order.quantity:
            buy_order.quantity -= sell_order.quantity
            order_history.append({"buy_order_id": buy_order.id, "sell_order_id": sell_order.id, "price": sell_order.price, "quantity": sell_order.quantity, "timestamp": time()})
            order_book["sell"].pop(0)
        elif buy_order.quantity < sell_order.quantity:
            sell_order.quantity -= buy_order.quantity
            order_history.append({"buy_order_id": buy_order.id, "sell_order_id": sell_order.id, "price": buy_order.price, "quantity": buy_order.quantity, "timestamp": time()})
            order_book["buy"].pop(0)
        else:
            order_history.append({"buy_order_id": buy_order.id, "sell_order_id": sell_order.id, "price": buy_order.price, "quantity": buy_order.quantity, "timestamp": time()})
            order_book["buy"].pop(0)
            order_book["sell"].pop(0)

@app.get("/orderhistory/")
async def get_orderhistory():
    global order_history
    return order_history

@app.get("/orderbook/")
async def get_orderbook():
    return order_book








# Add some sample orders
order_book["buy"].append(Order(id=str(uuid.uuid4()), type="buy", price=100.0, quantity=10.0))
order_book["sell"].append(Order(id=str(uuid.uuid4()), type="sell", price=110.0, quantity=5.0))
order_book["buy"].append(Order(id=str(uuid.uuid4()), type="buy", price=105.0, quantity=7.0))
order_book["sell"].append(Order(id=str(uuid.uuid4()), type="sell", price=120.0, quantity=3.0))
order_book["buy"].append(Order(id=str(uuid.uuid4()), type="buy", price=95.0, quantity=15.0))
order_book["sell"].append(Order(id=str(uuid.uuid4()), type="sell", price=125.0, quantity=10.0))
order_book["buy"].append(Order(id=str(uuid.uuid4()), type="buy", price=100.0, quantity=10.0))
order_book["sell"].append(Order(id=str(uuid.uuid4()), type="sell", price=130.0, quantity=5.0))




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=9999)



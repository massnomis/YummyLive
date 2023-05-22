from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
import uuid
import uvicorn
app = FastAPI()

class OrderType(str, Enum):
    buy = "buy"
    sell = "sell"

class Order(BaseModel):
    id: str
    type: OrderType
    price: float
    quantity: float
    # add timestamp

order_book = {
    "buy": [],
    "sell": []
}

@app.post("/order/")
async def create_order(order: Order):
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

def match_orders():
    while order_book["buy"] and order_book["sell"] and order_book["buy"][0].price >= order_book["sell"][0].price:
        buy_order = order_book["buy"][0]
        sell_order = order_book["sell"][0]
        if buy_order.quantity > sell_order.quantity:
            buy_order.quantity -= sell_order.quantity
            order_book["sell"].pop(0)
        elif buy_order.quantity < sell_order.quantity:
            sell_order.quantity -= buy_order.quantity
            order_book["buy"].pop(0)
        else:
            order_book["buy"].pop(0)
            order_book["sell"].pop(0)

@app.get("/orderbook/")
async def get_orderbook():
    return order_book

# Add some sample orders
order_book["buy"].append(Order(id=str(uuid.uuid4()), type="buy", price=100.0, quantity=10.0))
order_book["sell"].append(Order(id=str(uuid.uuid4()), type="sell", price=110.0, quantity=5.0))
order_book["buy"].append(Order(id=str(uuid.uuid4()), type="buy", price=105.0, quantity=7.0))
order_book["sell"].append(Order(id=str(uuid.uuid4()), type="sell", price=120.0, quantity=3.0))
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=9999)
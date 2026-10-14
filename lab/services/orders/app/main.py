from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.logging_config import setup_logging

app = FastAPI(title="orders-service")

logger = setup_logging()

# In-memory storage (temporary, will be replaced by Postgres)
orders: dict[int, dict] = {}

class OrderCreate(BaseModel):
    item: str
    quantity: int
    amount: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/orders")
def create_order(order: OrderCreate):
    order_id = len(orders) + 1
    new_order = {"id": order_id, **order.model_dump(), "status": "pending"}
    orders[order_id] = new_order
    logger.info(
        "order created",
        extra={"context": {"order_id": order_id, "item": order.item, "amount": order.amount}},
    )
    return new_order

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    if order_id not in orders:
        logger.warning(
            "order not found",
            extra={"context": {"order_id": order_id}},
        )
        raise HTTPException(status_code=404, detail="Order not found")
    return orders[order_id]

@app.get("/orders")
def list_orders():
    return list(orders.values())
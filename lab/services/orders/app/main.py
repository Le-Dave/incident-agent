from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.logging_config import setup_logging
from app.models import Order

app = FastAPI(title="orders-service")

logger = setup_logging()

# Create the tables in Postgres if they don't exist yet
Base.metadata.create_all(engine)

class OrderCreate(BaseModel):
    item: str
    quantity: int
    amount: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/orders")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    new_order = Order(**order.model_dump())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)  # reload to get the id chosen by Postgres
    logger.info(
        "order created",
        extra={"context": {"order_id": new_order.id, "item": order.item, "amount": order.amount}},
    )
    return new_order.to_dict()

@app.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if order is None:
        logger.warning(
            "order not found",
            extra={"context": {"order_id": order_id}},
        )
        raise HTTPException(status_code=404, detail="Order not found")
    return order.to_dict()

@app.get("/orders")
def list_orders(db: Session = Depends(get_db)):
    orders = db.scalars(select(Order).order_by(Order.id)).all()
    return [order.to_dict() for order in orders]

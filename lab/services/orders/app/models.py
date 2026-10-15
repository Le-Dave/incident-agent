from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Order(Base):
    """One row of the "orders" table."""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    item: Mapped[str] = mapped_column(String(200))
    quantity: Mapped[int]
    amount: Mapped[float]
    status: Mapped[str] = mapped_column(String(20), default="pending")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "item": self.item,
            "quantity": self.quantity,
            "amount": self.amount,
            "status": self.status,
        }

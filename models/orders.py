# models/order.py
from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    address = Column(String(255), nullable=False)
    status = Column(String(30), nullable=False)

    user = relationship("Users", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

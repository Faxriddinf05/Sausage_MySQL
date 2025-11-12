# models/order_item.py
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, autoincrement=True, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)

    product = relationship("Products", back_populates="order_items")
    order = relationship("Order", back_populates="order_items")

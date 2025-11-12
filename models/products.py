from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from db import Base


class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False)
    heading = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Integer, nullable=False)
    image = Column(String(255), nullable=True)

    order_items = relationship("OrderItem", back_populates="product")

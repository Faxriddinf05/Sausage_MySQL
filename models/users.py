from db import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)
    image = Column(String(255), nullable=True)

    orders = relationship("Order", back_populates="user")

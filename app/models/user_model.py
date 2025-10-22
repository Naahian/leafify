from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    recent_order = Column(String(255), nullable=True)
    my_plants = Column(JSON, nullable=True)

    # Relationships
    orders = relationship("Order", back_populates="user")

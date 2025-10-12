from sqlalchemy import Column, String, JSON
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    recent_order = Column(String, nullable=True)
    my_plants = Column(JSON, nullable=True)
    
    # Relationships
    orders = relationship("Order", back_populates="user")







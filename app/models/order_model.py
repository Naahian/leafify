from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    stock = Column(Integer, default=0)
    type = Column(String, nullable=False)  # 'plant' or 'accessory'
    
    # Relationships
    plant = relationship("Plant", back_populates="product", uselist=False)
    accessory = relationship("Accessory", back_populates="product", uselist=False)




class Order(Base):
    __tablename__ = "orders"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    products = Column(String, nullable=False)  # Could be JSON for product IDs
    total_price = Column(Float, nullable=False)
    transac_id = Column(String, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="orders")
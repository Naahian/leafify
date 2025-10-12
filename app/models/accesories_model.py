
from sqlalchemy import Column,  String,  ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Accessory(Base):
    __tablename__ = "accessories"
    
    id = Column(String, ForeignKey('products.id'), primary_key=True)
    size = Column(String, nullable=False)
    color = Column(String, nullable=False)
    
    # Relationships
    product = relationship("Product", back_populates="accessory")
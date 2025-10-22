from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Accessory(Base):
    __tablename__ = "accessories"

    id = Column(String(255), ForeignKey("products.id"), primary_key=True)
    size = Column(String(255), nullable=False)
    color = Column(String(255), nullable=False)

    # Relationships
    product = relationship("Product", back_populates="accessory")

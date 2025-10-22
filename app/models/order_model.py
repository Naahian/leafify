from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    stock = Column(Integer, default=0)
    type = Column(String(255), nullable=False)  # 'plant' or 'accessory'

    # Relationships
    plant = relationship("Plant", back_populates="product", uselist=False)
    accessory = relationship("Accessory", back_populates="product", uselist=False)

    def to_dict(self):
        """Convert Product model to dictionary matching ProductResponse schema"""
        result = {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "stock": self.stock,
            "type": self.type,
            "plant": None,
            "accessory": None,
        }

        # Add plant data if relationship is loaded and exists
        if self.plant is not None:
            result["plant"] = (
                self.plant.to_dict()
                if hasattr(self.plant, "to_dict")
                else {
                    "id": self.plant.id,
                    "category": self.plant.category,
                    "water": self.plant.water,
                    "light": self.plant.light,
                    "soil_type": self.plant.soil_type,
                    "size": self.plant.size,
                    # Add plant_guide if it exists
                    "plant_guide": (
                        self.plant.plant_guide.to_dict()
                        if self.plant.plant_guide
                        and hasattr(self.plant.plant_guide, "to_dict")
                        else None
                    ),
                }
            )

        if self.accessory is not None:
            result["accessory"] = (
                self.accessory.to_dict()
                if hasattr(self.accessory, "to_dict")
                else {
                    "id": self.accessory.id,
                    "color": self.accessory.color,
                    "size": self.accessory.size,
                }
            )

        return result


class Order(Base):
    __tablename__ = "orders"

    id = Column(String(255), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    products = Column(String(255), nullable=False)  # Could be JSON for product IDs
    total_price = Column(Float, nullable=False)
    transac_id = Column(String(255), nullable=False)

    # Relationships
    user = relationship("User", back_populates="orders")

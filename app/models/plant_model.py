from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base


class Plant(Base):
    __tablename__ = "plants"

    id = Column(String(255), ForeignKey("products.id"), primary_key=True)
    category = Column(String(255), nullable=False)
    water = Column(String(255), nullable=False)
    light = Column(String(255), nullable=False)
    soil_type = Column(String(255), nullable=False)
    size = Column(String(255), nullable=False)

    # Relationships
    product = relationship("Product", back_populates="plant")
    plant_guide = relationship("PlantGuide", back_populates="plant", uselist=False)


class PlantGuide(Base):
    __tablename__ = "plant_guides"

    id = Column(String(255), ForeignKey("plants.id"), primary_key=True)
    how_to_plant = Column(JSON, nullable=False)
    care_guide = Column(JSON, nullable=False)

    # Relationships
    plant = relationship("Plant", back_populates="plant_guide")

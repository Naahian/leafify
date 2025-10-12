from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Union


# Plant Schemas
class PlantBase(BaseModel):
    category: str
    water: str
    light: str
    soil_type: str
    size: str


class PlantCreate(PlantBase):
    id: str


class PlantUpdate(BaseModel):
    category: Optional[str] = None
    water: Optional[str] = None
    light: Optional[str] = None
    soil_type: Optional[str] = None
    size: Optional[str] = None


class PlantResponse(PlantBase):
    id: str
    
    class Config:
        from_attributes = True




# Accessory Schemas
class AccessoryBase(BaseModel):
    size: str
    color: str


class AccessoryCreate(AccessoryBase):
    id: str


class AccessoryUpdate(BaseModel):
    size: Optional[str] = None
    color: Optional[str] = None


class AccessoryResponse(AccessoryBase):
    id: str
    
    class Config:
        from_attributes = True


# Product Schemas
class ProductBase(BaseModel):
    name: str
    price: float = Field(..., gt=0)
    description: Optional[str] = None
    stock: int = Field(default=0, ge=0)
    type: str = Field(..., pattern="^(plant|accessory)$")


class ProductCreate(ProductBase):
    id: str


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None
    stock: Optional[int] = Field(None, ge=0)
    type: Optional[str] = Field(None, pattern="^(plant|accessory)$")


class ProductResponse(ProductBase):
    id: str
    plant: Optional[PlantWithGuide] = None
    accessory: Optional[AccessoryResponse] = None
    
    class Config:
        from_attributes = True


# For creating complete product with details
class CompletePlantProductCreate(BaseModel):
    product: ProductCreate
    plant: PlantCreate
    plant_guide: Optional[PlantGuideCreate] = None


class CompleteAccessoryProductCreate(BaseModel):
    product: ProductCreate
    accessory: AccessoryCreate
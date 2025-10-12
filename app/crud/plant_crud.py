from sqlalchemy.orm import Session
from app.models.plant_model import Plant
from app.schemas.product_schema import PlantCreate, PlantUpdate


def create_plant(db: Session, plant: PlantCreate):
    db_plant = Plant(**plant.dict())
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return db_plant


def get_all_plants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Plant).offset(skip).limit(limit).all()


def get_plant(db: Session, plant_id: str):
    return db.query(Plant).filter(Plant.id == plant_id).first()


def get_plants_by_category(db: Session, category: str):
    return db.query(Plant).filter(Plant.category == category).all()


def get_plants_by_water_needs(db: Session, water: str):
    return db.query(Plant).filter(Plant.water == water).all()


def get_plants_by_light_needs(db: Session, light: str):
    return db.query(Plant).filter(Plant.light == light).all()


def get_plants_by_size(db: Session, size: str):
    return db.query(Plant).filter(Plant.size == size).all()


def update_plant(db: Session, plant_id: str, plant: PlantUpdate):
    db_plant = get_plant(db, plant_id)
    if db_plant:
        for key, value in plant.dict(exclude_unset=True).items():
            setattr(db_plant, key, value)
        db.commit()
        db.refresh(db_plant)
    return db_plant


def delete_plant(db: Session, plant_id: str):
    db_plant = get_plant(db, plant_id)
    if db_plant:
        db.delete(db_plant)
        db.commit()
    return db_plant
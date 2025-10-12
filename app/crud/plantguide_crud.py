from sqlalchemy.orm import Session
from app.models.plant_model import PlantGuide
from app.schemas.plantguide_schema import PlantGuideCreate, PlantGuideUpdate


def create_plant_guide(db: Session, plant_guide: PlantGuideCreate):
    db_plant_guide = PlantGuide(**plant_guide.dict())
    db.add(db_plant_guide)
    db.commit()
    db.refresh(db_plant_guide)
    return db_plant_guide


def get_all_plant_guides(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PlantGuide).offset(skip).limit(limit).all()


def get_plant_guide(db: Session, plant_id: str):
    return db.query(PlantGuide).filter(PlantGuide.id == plant_id).first()


def update_plant_guide(db: Session, plant_id: str, plant_guide: PlantGuideUpdate):
    db_plant_guide = get_plant_guide(db, plant_id)
    if db_plant_guide:
        for key, value in plant_guide.dict(exclude_unset=True).items():
            setattr(db_plant_guide, key, value)
        db.commit()
        db.refresh(db_plant_guide)
    return db_plant_guide


def delete_plant_guide(db: Session, plant_id: str):
    db_plant_guide = get_plant_guide(db, plant_id)
    if db_plant_guide:
        db.delete(db_plant_guide)
        db.commit()
    return db_plant_guide
from sqlalchemy.orm import Session
from app.models.accesories_model import Accessory
from app.schemas.product_schema import AccessoryCreate, AccessoryUpdate


def create_accessory(db: Session, accessory: AccessoryCreate):
    db_accessory = Accessory(**accessory.dict())
    db.add(db_accessory)
    db.commit()
    db.refresh(db_accessory)
    return db_accessory


def get_all_accessories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Accessory).offset(skip).limit(limit).all()


def get_accessory(db: Session, accessory_id: str):
    return db.query(Accessory).filter(Accessory.id == accessory_id).first()


def get_accessories_by_size(db: Session, size: str):
    return db.query(Accessory).filter(Accessory.size == size).all()


def get_accessories_by_color(db: Session, color: str):
    return db.query(Accessory).filter(Accessory.color == color).all()


def update_accessory(db: Session, accessory_id: str, accessory: AccessoryUpdate):
    db_accessory = get_accessory(db, accessory_id)
    if db_accessory:
        for key, value in accessory.dict(exclude_unset=True).items():
            setattr(db_accessory, key, value)
        db.commit()
        db.refresh(db_accessory)
    return db_accessory


def delete_accessory(db: Session, accessory_id: str):
    db_accessory = get_accessory(db, accessory_id)
    if db_accessory:
        db.delete(db_accessory)
        db.commit()
    return db_accessory
from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate

class ItemCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_item(self, item: ItemCreate) -> Item:
        db_item = Item(**item.dict())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def get_item(self, item_id: int) -> Item:
        return self.db.query(Item).filter(Item.id == item_id).first()

    def update_item(self, item_id: int, item: ItemUpdate) -> Item:
        db_item = self.get_item(item_id)
        if db_item:
            for key, value in item.dict(exclude_unset=True).items():
                setattr(db_item, key, value)
            self.db.commit()
            self.db.refresh(db_item)
        return db_item

    def delete_item(self, item_id: int) -> Item:
        db_item = self.get_item(item_id)
        if db_item:
            self.db.delete(db_item)
            self.db.commit()
        return db_item

item_crud = ItemCRUD
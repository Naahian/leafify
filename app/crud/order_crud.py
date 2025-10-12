from sqlalchemy.orm import Session
from app.models import Order
from app.schemas.order_schema import OrderCreate, OrderUpdate


def create_order(db: Session, order: OrderCreate):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_all_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()


def get_order(db: Session, order_id: str):
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders_by_user(db: Session, user_id: str):
    return db.query(Order).filter(Order.user_id == user_id).all()


def get_order_by_transaction(db: Session, transac_id: str):
    return db.query(Order).filter(Order.transac_id == transac_id).first()


def update_order(db: Session, order_id: str, order: OrderUpdate):
    db_order = get_order(db, order_id)
    if db_order:
        for key, value in order.dict(exclude_unset=True).items():
            setattr(db_order, key, value)
        db.commit()
        db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: str):
    db_order = get_order(db, order_id)
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order


def get_user_total_spent(db: Session, user_id: str):
    orders = get_orders_by_user(db, user_id)
    return sum(order.total_price for order in orders)
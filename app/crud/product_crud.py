from uuid import uuid4
from sqlalchemy.orm import Session
from app.models.order_model import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate


def create_product(db: Session, product: ProductCreate):
    product_data = product.dict(exclude_unset=True)
    product_data["id"] = str(uuid4())
    db_product = Product(**product_data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_all_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()


def get_product(db: Session, product_id: str):
    return db.query(Product).filter(Product.id == product_id).first()


def get_product_by_name(db: Session, product_name: str):
    return db.query(Product).filter(Product.name == product_name).first()


def get_products_by_type(db: Session, product_type: str):
    return db.query(Product).filter(Product.type == product_type).all()


def get_products_in_stock(db: Session):
    return db.query(Product).filter(Product.stock > 0).all()


def update_product(db: Session, product_id: str, product: ProductUpdate):
    db_product = get_product(db, product_id)
    if db_product:
        for key, value in product.dict(exclude_unset=True).items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product


def update_product_stock(db: Session, product_id: str, stock_change: int):
    db_product = get_product(db, product_id)
    if db_product:
        db_product.stock += stock_change
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: str):
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

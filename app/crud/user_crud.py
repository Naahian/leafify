from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.auth_schema import UserCreate, UserUpdate
from app.services import get_password_hash
from uuid import uuid4


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    print(hashed_password)  # optional, for debugging

    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        phone=user.phone,
        address=user.address,
    )

    db.add(db_user)
    db.commit()

    db.refresh(db_user)
    return db_user


def get_all_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

from sqlalchemy.orm import Session
from app.models.auth import User
from app.schemas.auth import UserCreate, UserUpdate
from passlib import context


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(**user.dict(), password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

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

def get_password_hash(password):
    pwd_context = context.CryptContext(schemes=['bcrypt'], deprecated='auto')
    return pwd_context.hash(password)

def verify_password(password, hashed_password):
    pwd_context = context.CryptContext(schemes=['bcrypt'], deprecated='auto')
    return pwd_context.verify(password, hashed_password)
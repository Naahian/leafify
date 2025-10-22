import hashlib
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from typing import Optional

SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    sha256_digest = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    return pwd_context.verify(sha256_digest, hashed_password)


def get_password_hash(password: str) -> str:
    print(password)
    sha256_digest = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return pwd_context.hash(sha256_digest)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

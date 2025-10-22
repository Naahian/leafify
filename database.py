from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
ssl_args = {
    "ssl": {
        "ca": "ca.pem",
    }
}


engine = create_engine(
    DATABASE_URL,
    connect_args=ssl_args,
    pool_timeout=30,
    pool_recycle=3600,  # Recycle connections every hour
    pool_pre_ping=True,  # Verify connections before use
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_tables():
    print("Creating database tables...")

    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")

    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

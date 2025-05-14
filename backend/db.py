from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import dotenv
import os

dotenv.load_dotenv()
POSTGRES = os.getenv("POSTGRES")  

if not POSTGRES:
    raise ValueError("POSTGRES environment variable is not set")

SQLALCHEMY_DATABASE_URL = POSTGRES

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Corrected naming convention
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Table creation helper
def create_table():
    Base.metadata.create_all(bind=engine)

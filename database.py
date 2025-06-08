from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import dotenv
import os

dotenv.load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

print(DATABASE_URL)

engine = create_engine(DATABASE_URL, 
                       # connect_args={"sslmode": "require"}, 
                       # connect_args={"sslmode": "disable"}, 
                       pool_pre_ping=True)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
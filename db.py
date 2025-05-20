from sqlalchemy import create_engine, text
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

def drop_and_create_tables():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def alter_table_auto_increment():
    with engine.connect() as conn:
        # Create a sequence for the ID column
        conn.execute(text("""
            CREATE SEQUENCE IF NOT EXISTS veg_breakfast_lunch_id_seq;
        """))
        
        # Set the sequence as the default value for the id column
        conn.execute(text("""
            ALTER TABLE "Veg_Breakfast_Lunch" 
            ALTER COLUMN id SET DEFAULT nextval('veg_breakfast_lunch_id_seq');
        """))
        
        # Set the sequence to the current maximum id value
        conn.execute(text("""
            SELECT setval('veg_breakfast_lunch_id_seq', COALESCE((SELECT MAX(id) FROM "Veg_Breakfast_Lunch"), 1), false);
        """))
        
        conn.commit()


from sqlalchemy import text
from database import engine

def migrate_database():
    with engine.connect() as conn:
        # Check if tables exist
        check_tables = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('meals', 'additional_services', 'Veg_Breakfast_Lunch')
            );
        """)).scalar()

        if not check_tables:
            # Create tables only if they don't exist
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS meals (
                    id SERIAL PRIMARY KEY,
                    food_type VARCHAR(20) NOT NULL,
                    plan_type VARCHAR(20) NOT NULL,
                    num_people INTEGER NOT NULL,
                    basic_price NUMERIC NOT NULL,
                    basic_details TEXT,
                    frequency TEXT,
                    duration TEXT
                );

                CREATE TABLE IF NOT EXISTS additional_services (
                    id SERIAL PRIMARY KEY,
                    code VARCHAR(5),
                    name TEXT,
                    is_percentage BOOLEAN,
                    food_type VARCHAR(20),
                    plan_type VARCHAR(20),
                    meal_combo VARCHAR(40),
                    price_1 NUMERIC,
                    price_2 NUMERIC,
                    price_3 NUMERIC,
                    price_4 NUMERIC,
                    price_5 NUMERIC,
                    price_6 NUMERIC,
                    price_7 NUMERIC
                );

                CREATE TABLE IF NOT EXISTS meal_services (
                    meal_id INTEGER REFERENCES meals(id) ON DELETE CASCADE,
                    service_id INTEGER REFERENCES additional_services(id) ON DELETE CASCADE,
                    PRIMARY KEY (meal_id, service_id)
                );
            """))
            
            conn.commit()
            print("Tables created successfully")
        else:
            print("Tables already exist, skipping creation")

if __name__ == "__main__":
    migrate_database() 
import pandas as pd
from sqlalchemy import create_engine

try:

    df = pd.read_csv('C:/Users/HP/Downloads/area.csv')
    df.columns = df.columns.str.strip()

    engine = create_engine('')
    df.to_sql('areas', engine, if_exists='append', index=False)

    print("Success!")

except Exception:
    print("Unsuccessful")

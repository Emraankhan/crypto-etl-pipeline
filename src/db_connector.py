import os
import pandas as pd
from sqlalchemy import create_engine

def load_data_to_db(df):
    """
    Connects to AWS RDS and uploads the data.
    """
    if df.empty:
        print("DataFrame empty. Skipping load.")
        return

    try:
        # Get password and details from AWS Environment Variables
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        dbname = os.getenv("DB_NAME")

        # Create connection string
        db_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        engine = create_engine(db_url)

        # Upload data
        # 'append' means add new rows, don't delete old ones
        df.to_sql('crypto_prices', engine, if_exists='append', index=False)
        print("Data loaded to Database successfully!")
        
    except Exception as e:
        print(f"Database Error: {e}")
        raise e
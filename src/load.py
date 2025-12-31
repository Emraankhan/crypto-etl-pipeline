import pandas as pd
from sqlalchemy import text
from src.db_connector import get_db_engine

def load_data_to_db(df, table_name="crypto_prices"):
    """
    Loads the cleaned DataFrame into PostgreSQL.
    """
    engine = get_db_engine()
    if engine is None:
        print("Skipping load due to connection error.")
        return

    # 1. Create Table if it doesn't exist (DDL)
    # We define a Composite Primary Key (coin_id + updated_at) to prevent duplicates
    create_table_query = text(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            coin_id VARCHAR(50),
            price_usd DECIMAL(18, 2),
            price_eur DECIMAL(18, 2),
            updated_at TIMESTAMP,
            PRIMARY KEY (coin_id, updated_at)
        );
    """)

    with engine.connect() as conn:
        conn.execute(create_table_query)
        conn.commit()

    # 2. Insert Data
    try:
        # 'append' adds new rows. 
        # Note: If a row with the same Primary Key exists, this simple method might fail.
        # For a production system, we would handle 'ON CONFLICT' here. 
        # For now, we use a try-except block to catch duplicates.
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"[OK] Successfully loaded {len(df)} rows into '{table_name}'.")
        
    except Exception as e:
        # If we try to insert a duplicate, Postgres will complain.
        if "unique constraint" in str(e).lower():
            print("⚠️ Notice: Some data already exists in the DB (Duplicate skipped).")
        else:
            print(f"❌ Error loading data: {e}")

# Test block
if __name__ == "__main__":
    # Create dummy data to test loading
    data = {
        'coin_id': ['bitcoin', 'ethereum'],
        'price_usd': [50000.00, 3000.00],
        'price_eur': [45000.00, 2700.00],
        'updated_at': ['2023-11-14 10:00:00', '2023-11-14 10:00:00']
    }
    df = pd.DataFrame(data)
    load_data_to_db(df)
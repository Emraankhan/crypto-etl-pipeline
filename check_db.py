import pandas as pd
from src.db_connector import get_db_engine

def view_data():
    engine = get_db_engine()
    print("\n--- Connecting to Database ---")
    try:
        # Select the last 10 rows, sorted by time
        query = "SELECT * FROM crypto_prices ORDER BY updated_at DESC LIMIT 10;"
        df = pd.read_sql(query, engine)
        
        if df.empty:
            print("⚠️ The database is connected, but the table is empty.")
        else:
            print(df)
            print("\n✅ Verification Complete: Data is persisting!")
            
    except Exception as e:
        print(f"❌ Error reading data: {e}")

if __name__ == "__main__":
    view_data()
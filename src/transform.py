import pandas as pd
from datetime import datetime

def process_crypto_data(data):
    """
    Transforms raw JSON data into a clean DataFrame.
    """
    if not data:
        print("No data to transform.")
        return pd.DataFrame()

    try:
        df = pd.DataFrame(data)
        
        # Keep only the columns we need
        # (We use .get to avoid errors if a column is missing)
        clean_data = []
        for index, row in df.iterrows():
            clean_data.append({
                'symbol': row.get('symbol'),
                'name': row.get('name'),
                'current_price': row.get('current_price'),
                'market_cap': row.get('market_cap'),
                'total_volume': row.get('total_volume'),
                'last_updated': row.get('last_updated'),
                'ingested_at': datetime.utcnow()
            })
            
        df_clean = pd.DataFrame(clean_data)
        print(f"Transformed {len(df_clean)} rows.")
        return df_clean
        
    except Exception as e:
        print(f"Error in transformation: {e}")
        return pd.DataFrame()
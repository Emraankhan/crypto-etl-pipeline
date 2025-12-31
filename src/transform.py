import pandas as pd
from datetime import datetime

def transform_data(raw_data):
    """
    Transforms raw JSON data into a clean Pandas DataFrame.
    1. Flattens the nested dictionary.
    2. Converts Unix timestamps to readable Datetime objects.
    """
    if not raw_data:
        print("⚠️ No data to transform.")
        return None

    data_list = []

    # Loop through the dictionary (key = coin name, value = price details)
    for coin_name, details in raw_data.items():
        # Create a clean row for each coin
        row = {
            'coin_id': coin_name,
            'price_usd': details.get('usd'),
            'price_eur': details.get('eur'),
            # Convert Unix timestamp (seconds) to datetime
            'updated_at': datetime.fromtimestamp(details.get('last_updated_at')) 
        }
        data_list.append(row)

    # Convert list of dicts to a Pandas DataFrame
    df = pd.DataFrame(data_list)

    # Simple Data Quality Check
    if df.isnull().values.any():
        print("⚠️ Warning: Missing values detected!")
        df = df.dropna() # Option: Drop rows with missing data
    
    print(f"✅ Data transformed successfully! ({len(df)} records)")
    return df

# Test block
if __name__ == "__main__":
    # We create dummy data to test this script independently
    dummy_data = {
        'bitcoin': {'usd': 50000, 'eur': 45000, 'last_updated_at': 1700000000},
        'solana': {'usd': 100, 'eur': 90, 'last_updated_at': 1700000000}
    }
    clean_df = transform_data(dummy_data)
    print("\nPreview of Clean Data:")
    print(clean_df)
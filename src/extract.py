import requests
import logging

def fetch_crypto_data():
    """
    Fetches the top 50 cryptocurrencies from CoinGecko API.
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": "false"
    }
    
    try:
        print("Fetching data from API...")
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status() # Check for errors (404, 500)
        data = response.json()
        print(f"Successfully fetched {len(data)} records.")
        return data
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []
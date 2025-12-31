import requests
import json

def get_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "usd,eur",
        "include_last_updated_at": "true"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Check for errors (404, 500)
        data = response.json()
        
        # Pretty print the JSON
        print(json.dumps(data, indent=4))
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    get_bitcoin_price()
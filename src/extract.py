import requests
import yaml
import os
import sys

# Load Configuration securely
def load_config():
    # Gets the absolute path of the project root to find the config file reliably
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    config_path = os.path.join(project_root, 'config', 'settings.yaml')
    
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: Config file not found at {config_path}")
        sys.exit(1)

def extract_data():
    """
    Fetches data from the CoinGecko API based on settings.yaml.
    Returns: JSON data (dictionary) or None if failed.
    """
    config = load_config()
    url = config['api']['url']
    
    # Parameters for the API call
    params = {
        "ids": config['api']['coins'],
        "vs_currencies": config['api']['currencies'],
        "include_last_updated_at": "true"
    }

    try:
        print(f"Connecting to {url}...")
        response = requests.get(url, params=params, timeout=10) # 10 second timeout
        response.raise_for_status() # Raises error for 404, 500, etc.
        
        data = response.json()
        print("✅ Data extraction successful!")
        return data

    except requests.exceptions.RequestException as e:
        print(f"❌ API Request failed: {e}")
        return None

# This allows us to test this script individually
if __name__ == "__main__":
    raw_data = extract_data()
    print(raw_data)
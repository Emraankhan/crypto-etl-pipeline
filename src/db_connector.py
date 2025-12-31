import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path

# --- FIX START ---
# Get the base directory of the project (one level up from 'src')
base_dir = Path(__file__).resolve().parent.parent
# Explicitly point to the .env file
env_path = base_dir / '.env'
load_dotenv(dotenv_path=env_path)
# --- FIX END ---

def get_db_engine():
    """
    Constructs the database URL from environment variables 
    and returns a SQLAlchemy engine.
    """
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    dbname = os.getenv("DB_NAME")

    # Debugging: Check if variables are loaded
    if not all([user, password, host, port, dbname]):
        print(f"❌ Error: Missing environment variables! Checked path: {env_path}")
        print(f"User: {user}, Port: {port}, Host: {host}") # Print to see what's missing
        return None

    # Construct the connection string
    url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    
    try:
        engine = create_engine(url)
        # Test the connection properly
        with engine.connect() as conn:
            pass
        return engine
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None
import logging
import sys
import os
from src.extract import fetch_crypto_data
from src.transform import process_crypto_data
from src.db_connector import load_data_to_db

# Configure Logging (Cloud Safe Version)
# We ONLY write to sys.stdout (The Screen), not to a file.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def run_etl():
    """The core logic of our pipeline"""
    logger.info("--- [START] Starting ETL Job ---")
    try:
        # 1. Extract
        raw_data = fetch_crypto_data()
        if not raw_data:
            logger.warning("No data extracted. Skipping job.")
            return {"statusCode": 200, "body": "No Data"}
            
        # 2. Transform
        df_transformed = process_crypto_data(raw_data)
        
        # 3. Load
        load_data_to_db(df_transformed)
        
        logger.info("[SUCCESS] ETL Job Completed Successfully.")
        return {"statusCode": 200, "body": "Success"}
        
    except Exception as e:
        logger.error(f"ETL Job Failed: {e}")
        # In Lambda, we don't want to crash the whole bot, just report the error
        return {"statusCode": 500, "body": str(e)}

# --- AWS LAMBDA HANDLER ---
def lambda_handler(event, context):
    return run_etl()

# --- LOCAL RUN ---
if __name__ == "__main__":
    run_etl()
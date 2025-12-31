import time
import schedule
import logging
import sys
import os
from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data_to_db

# --- DEBUGGING: WHERE IS THE FILE? ---
log_file_path = os.path.abspath("pipeline.log")
print(f"🔎 DEBUG: Log file is being saved here: {log_file_path}")

# --- CONFIGURATION: LOGGING ---
# We use force=True to reset any old loggers
# We use encoding='utf-8' for emoji safety
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ],
    force=True 
)

def job():
    """
    The main ETL function.
    """
    logging.info("--- [START] Starting ETL Job ---")
    
    try:
        # Step 1: Extract
        raw_data = extract_data()
        
        # Step 2: Transform
        if raw_data:
            clean_df = transform_data(raw_data)
            
            # Step 3: Load
            if clean_df is not None:
                load_data_to_db(clean_df)
                logging.info("[SUCCESS] ETL Job Completed Successfully.")
            else:
                logging.warning("[WARN] Transformation failed, skipping load.")
        else:
            logging.warning("[WARN] No data extracted, skipping pipeline.")
            
    except Exception as e:
        logging.error(f"[ERROR] Critical Pipeline Error: {e}")

# --- IMMEDIATE TEST ---
# We write a test log right now to prove it works
logging.info("📝 TEST LOG: If you can see this in the file, logging is fixed!")

# --- SCHEDULING ---
job()
schedule.every(1).minutes.do(job)

logging.info("[WAIT] Pipeline scheduler started. Waiting for next job...")

while True:
    schedule.run_pending()
    time.sleep(1)
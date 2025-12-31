import time
import schedule
from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data_to_db

def job():
    """
    The main ETL function. 
    It runs the Extract -> Transform -> Load steps in sequence.
    """
    print(f"\n--- Starting ETL Job at {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
    
    # Step 1: Extract
    raw_data = extract_data()
    
    # Step 2: Transform
    if raw_data:
        clean_df = transform_data(raw_data)
        
        # Step 3: Load
        if clean_df is not None:
            load_data_to_db(clean_df)
    
    print("--- Job Finished ---")

# --- Scheduling Configuration ---
# Run the job immediately once (so we don't have to wait 1 minute to see if it works)
job()

# Schedule the job to run every 1 minute
schedule.every(1).minutes.do(job)

print("\n🚀 Pipeline is running! (Press Ctrl+C to stop)")

# Keep the script running to maintain the schedule
while True:
    schedule.run_pending()
    time.sleep(1)
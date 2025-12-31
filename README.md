# 🚀 Real-Time Cryptocurrency ETL Pipeline

## 📌 Project Overview
A fully containerized Data Engineering pipeline that ingests real-time financial data, processes it for insights, and warehouses it in a PostgreSQL database.

This project simulates a production-grade environment where data consistency, automation, and infrastructure-as-code are paramount. It acts as a history tracker for Bitcoin, Ethereum, and Solana prices, enabling trend analysis and volatility reporting.

**Key Engineering Concepts:**
* **Real-Time Extraction:** Connects to external APIs (CoinGecko) to fetch live market data.
* **Idempotent Loading:** Prevents duplicate data entries using Composite Primary Keys, ensuring data integrity even if the pipeline re-runs accidentally.
* **Containerization:** The entire database infrastructure runs in Docker, ensuring consistent environments across machines.
* **Automated Reporting:** Includes an analytics module (`analytics.py`) that generates instant volatility and trend reports using SQL & Pandas.

---

## 🛠️ Tech Stack
* **Language:** Python 3.12
* **Containerization:** Docker & Docker Compose
* **Database:** PostgreSQL 15
* **Libraries:** Pandas, SQLAlchemy, Schedule, Requests, Python-Dotenv
* **Orchestration:** Python-based Cron Scheduler

---

## 🏗️ Architecture
1.  **Extract Service:** Python script hits the CoinGecko API every 60 seconds.
2.  **Transform Service:** Cleans JSON data, converts Unix timestamps to UTC, and validates data types.
3.  **Load Service:** Inserts data into PostgreSQL. Uses `INSERT ... ON CONFLICT DO NOTHING` logic to handle duplicates.
4.  **Analyze Service:** Connects to the warehouse to calculate averages, volatility, and market trends.

---

## ⚙️ How to Run Locally

### 1. Prerequisites
* Docker Desktop installed
* Python 3.10+ installed
* Git

### 2. Setup
Clone the repository and install dependencies:
```bash
git clone [https://github.com/YOUR_USERNAME/crypto-etl-pipeline.git](https://github.com/Emraankhan/crypto-etl-pipeline.git)
cd crypto-etl-pipeline
pip install -r requirements.txt


3. Configuration
Create a .env file in the root directory (This file is ignored by Git for security):

DB_USER=user
DB_PASSWORD=admin123
DB_HOST=127.0.0.1
DB_PORT=5433
DB_NAME=crypto_db


4. Start the Infrastructure
Launch the PostgreSQL database container:

docker-compose up -d


5. Run the Pipeline
Start the automated ETL job (Press Ctrl+C to stop):

python main.py

The script will run continuously, fetching data every minute.


6. Generate Reports
To view current market insights and volatility analysis:

python analytics.py


📊 Sample Output
ETL Log:

--- Starting ETL Job at 2025-12-31 19:29:17 ---
✅ Data extraction successful!
✅ Data transformed successfully! (3 records)
[OK] Successfully loaded 3 rows into 'crypto_prices'.


Analytics Report (python analytics.py):

1. Market Trend Analysis:
    coin_id  current_price  average_price   trend
0   bitcoin       87806.00       87500.00   🚀 UP
1  ethereum        2976.44        2980.00   🔻 DOWN

2. Volatility Report:
    coin_id  min_price  max_price  price_swing
0   bitcoin   87200.00   87848.00       648.00


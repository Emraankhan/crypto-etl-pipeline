# 🚀 Serverless Crypto ETL Pipeline

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://crypto-etl-pipeline.streamlit.app/)

**Live Dashboard:** [https://crypto-etl-pipeline.streamlit.app/](https://crypto-etl-pipeline.streamlit.app/)

## 📖 Overview
This project is a fully automated, serverless data pipeline that extracts cryptocurrency data, stores it in a Cloud Database, and visualizes it on a live Dashboard.

It demonstrates a modern **Cloud-Native** architecture using **AWS**, **Docker**, and **Python**.

## 🏗️ Architecture
The pipeline follows a modern Extract, Transform, Load (ETL) workflow:

**Flow:** `CoinGecko API` ➡ `AWS Lambda (Docker)` ➡ `AWS RDS (PostgreSQL)` ➡ `Streamlit Dashboard`

1.  **Extract:** A Python script fetches live market data for the top 50 cryptocurrencies via the **CoinGecko API**.
2.  **Transform:** Data is cleaned, structured, and timestamped using **Pandas**.
3.  **Load:** The processed data is securely inserted into an **AWS RDS (PostgreSQL)** database.
4.  **Automation:** **Amazon EventBridge** triggers the Lambda function every day at 9:00 AM.
5.  **Visualization:** A **Streamlit** dashboard connects to the cloud database to visualize trends and KPIs.

## 🛠️ Tech Stack
* **Cloud Provider:** AWS (eu-central-1)
* **Compute:** AWS Lambda (Serverless)
* **Containerization:** Docker & Amazon ECR
* **Database:** AWS RDS (PostgreSQL)
* **Orchestration:** Amazon EventBridge (Scheduler)
* **Language:** Python 3.12
* **Libraries:** `pandas`, `psycopg2`, `sqlalchemy`, `streamlit`, `plotly`

## 📂 Project Structure
```text
├── src/
│   ├── extract.py       # Connects to CoinGecko API
│   ├── transform.py     # Cleans and structures the data
│   ├── load.py          # Inserts data into PostgreSQL
│   ├── db_connector.py  # Manages database connections
│   └── main.py          # Lambda Handler (Entry point)
├── Dockerfile.aws       # Instructions for building the Lambda Container
├── dashboard.py         # Live Data Visualization App
├── requirements.txt     # Python dependencies
└── README.md            # Project Documentation


🚀 How to Run Locally (Dashboard)
To view the live dashboard on your local machine:

1. Clone the repository:
git clone [https://github.com/Emraankhan/crypto-etl-pipeline.git](https://github.com/Emraankhan/crypto-etl-pipeline.git)
cd crypto-etl-pipeline

2. Install Dependencies:
pip install -r requirements.txt

3. Configure Environment: Create a .env file in the root directory with your AWS RDS credentials (do not share this file):

DB_HOST=your-db-endpoint.rds.amazonaws.com
DB_NAME=crypto_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432

### 4. Launch Dashboard:
python -m streamlit run dashboard.py


☁️ Deployment Logic
The ETL logic is packaged as a Docker container to ensure consistency between development and production.

1. Build Image: docker build -f Dockerfile.aws -t crypto-etl .

2. Push to ECR: Tag and push the image to Amazon Elastic Container Registry.

3. Deploy Lambda: Update the Lambda function to use the new container image.
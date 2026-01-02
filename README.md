# 🚀 Serverless Crypto ETL Pipeline

## 📖 Overview
This project is a fully automated, serverless data pipeline that extracts cryptocurrency data, stores it in a Cloud Database, and visualizes it on a live Dashboard.

It demonstrates a modern **Cloud-Native** architecture using **AWS**, **Docker**, and **Python**.

## 🏗️ Architecture
**Flow:** `CoinGecko API` -> `AWS Lambda (Docker)` -> `AWS RDS (PostgreSQL)` -> `Streamlit Dashboard`

* **Source:** CoinGecko API (Extracts top 50 Cryptos).
* **Compute:** AWS Lambda (Runs Python code wrapped in Docker).
* **Storage:** AWS RDS (PostgreSQL Database).
* **Automation:** Amazon EventBridge (Triggers the job daily at 9:00 AM).
* **Visualization:** Streamlit Dashboard (Connects to Cloud DB).

## 🛠️ Tech Stack
* **Cloud:** AWS (Lambda, RDS, ECR, EventBridge, IAM).
* **Containerization:** Docker.
* **Language:** Python 3.12.
* **Libraries:** Pandas, SQLAlchemy, Plotly, Streamlit.
* **Infrastructure as Code:** Dockerfile for Lambda environment.

## 📂 Project Structure
```text
├── src/
│   ├── extract.py       # API connection logic
│   ├── transform.py     # Data cleaning & Pandas logic
│   ├── load.py          # Database insertion logic
│   └── main.py          # Lambda Handler (Entry point)
├── Dockerfile.aws       # Instructions for building the Cloud Container
├── dashboard.py         # Live Data Visualization App
├── requirements.txt     # Project Dependencies
└── README.md            # Documentation


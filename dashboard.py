import streamlit as st
import pandas as pd
import os
import time
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv

# --- 1. SETUP & SECRETS ---
st.set_page_config(
    page_title="Crypto Cloud HQ", 
    page_icon="🚀", 
    layout="wide"
)
load_dotenv()

# --- 2. CONNECT TO CLOUD DATABASE ---
def get_db_connection():
    try:
        # Construct the connection URL directly here
        # (This removes the dependency on src.db_connector)
        db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        engine = create_engine(db_url)
        return engine
    except Exception as e:
        return None

# --- 3. LOAD DATA ---
def get_data():
    engine = get_db_connection()
    if not engine:
        st.error("❌ Could not connect to AWS Database. Check your .env file!")
        return pd.DataFrame()

    # Get the MOST RECENT snapshot of data
    query = """
    SELECT symbol, name, current_price, market_cap, total_volume, last_updated 
    FROM crypto_prices 
    ORDER BY ingested_at DESC 
    LIMIT 50;
    """
    try:
        return pd.read_sql(query, engine)
    except Exception as e:
        st.error(f"Error reading data: {e}")
        return pd.DataFrame()

# --- 4. DASHBOARD LAYOUT ---
st.title("🚀 Crypto Cloud Dashboard")
st.caption("Live Data from AWS RDS (PostgreSQL)")

# Sidebar for Refresh
with st.sidebar:
    st.header("Controls")
    if st.button("🔄 Refresh Data", type="primary"):
        st.rerun()
    st.info("Data updates every morning at 9:00 AM via AWS Lambda.")

# Load Data
df = get_data()

if not df.empty:
    # --- KPI METRICS ---
    # We grab specific coins to show at the top
    col1, col2, col3, col4 = st.columns(4)
    
    # Helper to find price safely
    def get_price(symbol):
        row = df[df['symbol'] == symbol]
        if not row.empty:
            return row['current_price'].values[0]
        return 0

    col1.metric("Bitcoin (BTC)", f"${get_price('btc'):,.2f}")
    col2.metric("Ethereum (ETH)", f"${get_price('eth'):,.2f}")
    col3.metric("Solana (SOL)", f"${get_price('sol'):,.2f}")
    col4.metric("BNB", f"${get_price('bnb'):,.2f}")

    st.markdown("---")

    # --- CHARTS ---
    col_chart, col_table = st.columns([2, 1])

    with col_chart:
        st.subheader("📊 Market Cap Leaders")
        # Top 10 for the chart
        top_10 = df.head(10)
        fig = px.bar(
            top_10, 
            x='name', 
            y='market_cap', 
            color='market_cap',
            color_continuous_scale='Viridis',
            labels={'market_cap': 'Market Cap ($)', 'name': 'Asset'}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_table:
        st.subheader("📋 Top 20 Assets")
        # Display a clean table of the top 20
        st.dataframe(
            df.head(20)[['name', 'current_price', 'market_cap']], 
            hide_index=True,
            use_container_width=True
        )
else:
    st.warning("No data found. Please run your Lambda function once to populate the database!")
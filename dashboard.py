import streamlit as st
import pandas as pd
import plotly.express as px
from src.db_connector import get_db_engine

# 1. Page Config
st.set_page_config(page_title="Crypto ETL Dashboard", page_icon="📈", layout="wide")
st.title("🔴 Live Crypto ETL Dashboard")

# 2. Auto-Refresh Logic (Every 3 seconds)
if st.button("🔄 Refresh Data"):
    st.rerun()

# 3. Connect to Database
@st.cache_data(ttl=5) # Cache data for 5 seconds to prevent database spam
def load_data():
    engine = get_db_engine()
    query = """
    SELECT coin_id, price_usd, updated_at 
    FROM crypto_prices 
    ORDER BY updated_at ASC
    """
    return pd.read_sql(query, engine)

try:
    df = load_data()

    # 4. Key Metrics (The "Ticker" at the top)
    # Get the latest prices
    latest_df = df.sort_values(by='updated_at').groupby('coin_id').tail(1)
    
    col1, col2, col3 = st.columns(3)
    
    # Bitcoin Metric
    btc_price = latest_df[latest_df['coin_id'] == 'bitcoin']['price_usd'].values[0]
    col1.metric("Bitcoin (BTC)", f"${btc_price:,.2f}")

    # Ethereum Metric
    eth_price = latest_df[latest_df['coin_id'] == 'ethereum']['price_usd'].values[0]
    col2.metric("Ethereum (ETH)", f"${eth_price:,.2f}")
    
    # Solana Metric
    sol_price = latest_df[latest_df['coin_id'] == 'solana']['price_usd'].values[0]
    col3.metric("Solana (SOL)", f"${sol_price:,.2f}")

    # 5. Charts
    st.subheader("Price History")
    
    # Create an interactive line chart
    fig = px.line(df, x='updated_at', y='price_usd', color='coin_id', 
                  title="Cryptocurrency Price Trends (USD)",
                  markers=True)
    
    st.plotly_chart(fig, use_container_width=True)

    # 6. Raw Data View
    with st.expander("View Raw Data"):
        st.dataframe(df.sort_values(by='updated_at', ascending=False))

except Exception as e:
    st.error(f"Error connecting to database: {e}")
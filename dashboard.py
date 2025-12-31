import streamlit as st
import pandas as pd
import plotly.express as px
import time
from src.db_connector import get_db_engine

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Crypto ETL HQ", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Pro" look
st.markdown("""
    <style>
    .stMetric {
        background-color: #0E1117;
        border: 1px solid #262730;
        padding: 10px;
        border-radius: 5px;
    }
    .stDataFrame {
        border: 1px solid #262730;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("🎛️ Control Panel")
    
    # A. Time Filter
    st.subheader("Time Range")
    time_range = st.radio(
        "Select Data Window:",
        ["1 Hour", "6 Hours", "24 Hours", "All Time"],
        index=3 # Default to "All Time" so you see data immediately
    )

    # B. Auto-Refresh
    st.subheader("Real-Time Mode")
    enable_autorefresh = st.toggle("⚡ Enable Live Updates")
    refresh_rate = st.slider("Refresh Rate (seconds)", 2, 60, 5)

    # C. Coin Filter
    st.subheader("Assets")
    selected_coins = st.multiselect(
        "Filter Coins:", 
        ['bitcoin', 'ethereum', 'solana'], 
        default=['bitcoin', 'ethereum', 'solana']
    )
    
    st.markdown("---")
    st.caption("v2.0 | Built with Python & Docker")

# --- 3. DATA LOADING LOGIC ---
def get_data(window):
    engine = get_db_engine()
    
    # Logic to filter by time in SQL
    if window == "1 Hour":
        interval = "INTERVAL '1 hour'"
    elif window == "6 Hours":
        interval = "INTERVAL '6 hours'"
    elif window == "24 Hours":
        interval = "INTERVAL '24 hours'"
    else:
        interval = "INTERVAL '10 years'" # Effectively "All Time"

    query = f"""
    SELECT coin_id, price_usd, updated_at 
    FROM crypto_prices 
    WHERE updated_at >= NOW() - {interval}
    ORDER BY updated_at ASC
    """
    
    return pd.read_sql(query, engine)

# --- 4. MAIN DASHBOARD ---
st.title("🚀 Crypto Data Engineering Pipeline")
st.markdown(f"**Viewing Data:** Last {time_range} | **Mode:** {'🟢 Live' if enable_autorefresh else '🔴 Static'}")

try:
    # Fetch Data
    df = get_data(time_range)
    
    # Filter by user selection
    if not selected_coins:
        st.error("⚠️ Please select at least one coin in the sidebar.")
    else:
        df_filtered = df[df['coin_id'].isin(selected_coins)]

        if df_filtered.empty:
            st.warning(f"No data found for the last {time_range}. Try selecting 'All Time'.")
        else:
            # --- METRICS SECTION ---
            # We calculate specific stats for the selected window
            st.markdown("### 💵 Asset Performance")
            
            # Create dynamic columns based on selected coins
            cols = st.columns(len(selected_coins))
            
            for idx, coin in enumerate(selected_coins):
                coin_data = df_filtered[df_filtered['coin_id'] == coin]
                if not coin_data.empty:
                    current = coin_data.iloc[-1]['price_usd']
                    high = coin_data['price_usd'].max()
                    low = coin_data['price_usd'].min()
                    
                    # Calculate change
                    start = coin_data.iloc[0]['price_usd']
                    change = current - start
                    
                    with cols[idx]:
                        st.metric(
                            label=f"{coin.upper()}",
                            value=f"${current:,.2f}",
                            delta=f"${change:+.2f}"
                        )
                        st.caption(f"Low: ${low:,.0f} | High: ${high:,.0f}")

            st.divider()

            # --- CHARTS SECTION ---
            tab1, tab2 = st.tabs(["📈 Price Trends", "📊 Volatility Analysis"])
            
            with tab1:
                fig = px.area(
                    df_filtered, 
                    x='updated_at', 
                    y='price_usd', 
                    color='coin_id',
                    template='plotly_dark',
                    color_discrete_map={'bitcoin': '#F7931A', 'ethereum': '#627EEA', 'solana': '#14F195'}
                )
                fig.update_layout(xaxis_title="Time", yaxis_title="Price (USD)", height=500)
                st.plotly_chart(fig, use_container_width=True)

            with tab2:
                # Box plot to show price distribution/volatility
                fig_vol = px.box(
                    df_filtered, 
                    x='coin_id', 
                    y='price_usd', 
                    color='coin_id',
                    template='plotly_dark',
                    title="Price Distribution (Volatility Range)"
                )
                st.plotly_chart(fig_vol, use_container_width=True)

            # --- DATA EXPORT ---
            with st.expander("📥 Download Raw Data"):
                csv = df_filtered.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name='crypto_data_export.csv',
                    mime='text/csv',
                )

    # --- AUTO REFRESH LOGIC ---
    if enable_autorefresh:
        time.sleep(refresh_rate)
        st.rerun()

except Exception as e:
    st.error(f"Error: {e}")
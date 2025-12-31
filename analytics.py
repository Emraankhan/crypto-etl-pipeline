import pandas as pd
from src.db_connector import get_db_engine

def run_analytics():
    engine = get_db_engine()
    print("\n--- 📊 CRYPTO MARKET INSIGHTS ---\n")

    # Insight 1: Current Trends (Latest Price vs Average)
    # We check if the latest price is higher or lower than the average of all time.
    print("1. Market Trend Analysis (Latest vs. Average):")
    query_trend = """
    SELECT 
        coin_id,
        MAX(updated_at) as last_update,
        -- Get the price from the most recent timestamp
        (SELECT price_usd FROM crypto_prices p2 WHERE p2.coin_id = p1.coin_id ORDER BY updated_at DESC LIMIT 1) as current_price,
        AVG(price_usd) as average_price
    FROM crypto_prices p1
    GROUP BY coin_id;
    """
    df_trend = pd.read_sql(query_trend, engine)
    
    # Let's add a calculated column using Pandas
    df_trend['trend'] = df_trend.apply(
        lambda row: '🚀 UP' if row['current_price'] > row['average_price'] else '🔻 DOWN', axis=1
    )
    print(df_trend[['coin_id', 'current_price', 'average_price', 'trend']])

    # Insight 2: Volatility (Highs and Lows)
    print("\n2. Volatility Report (Min vs Max):")
    query_volatility = """
    SELECT 
        coin_id,
        MIN(price_usd) as min_price,
        MAX(price_usd) as max_price,
        MAX(price_usd) - MIN(price_usd) as price_swing
    FROM crypto_prices
    GROUP BY coin_id;
    """
    df_vol = pd.read_sql(query_volatility, engine)
    print(df_vol)

if __name__ == "__main__":
    run_analytics()
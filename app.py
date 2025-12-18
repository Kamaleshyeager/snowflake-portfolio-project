import streamlit as st
import pandas as pd
import plotly.express as px
from snowflake_connector import init_connection, run_query
import datetime
import numpy as np

st.set_page_config(page_title="Snowflake Retail Analytics", page_icon="❄️", layout="wide")
st.markdown("""<style>.metric-card {background-color: #f0f2f6;padding: 20px;border-radius: 10px;box-shadow: 2px 2px 10px rgba(0,0,0,0.05);text-align: center;}.stApp header {background-color: transparent;}</style>""", unsafe_allow_html=True)
col1, col2 = st.columns([1, 5])
with col1: st.image("https://www.snowflake.com/wp-content/uploads/2017/08/Snowflake_Logo_blue-1.png", width=100)
with col2: st.title("Executive Retail Dashboard"); st.markdown("*Powered by Snowflake & Streamlit*")
st.divider()
use_mock_data = False
if "snowflake" not in st.secrets:
    st.warning("⚠️ No Snowflake credentials found. Running in **Demo Mode**."); use_mock_data = True
else:
    conn = init_connection()
    if conn is None: st.error("❌ Failed to connect."); st.stop()
    else: st.success("✅ Connected to Snowflake")

def get_data(mock=False):
    if mock:
        dates = pd.date_range(start="2023-01-01", end="2023-12-31")
        sales = np.random.randint(1000, 5000, size=len(dates))
        categories = np.random.choice(['Electronics', 'Furniture', 'Clothing', 'Books'], size=len(dates))
        return pd.DataFrame({'ORDER_DATE': dates, 'SALES_AMOUNT': sales, 'CATEGORY': categories})
    else:
        query = """SELECT O_ORDERDATE as ORDER_DATE, O_TOTALPRICE as SALES_AMOUNT, CASE WHEN O_CLERK LIKE '%001%' THEN 'Electronics' WHEN O_CLERK LIKE '%002%' THEN 'Furniture' WHEN O_CLERK LIKE '%003%' THEN 'Clothing' ELSE 'Books' END as CATEGORY FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS SAMPLE(1) LIMIT 1000"""
        return run_query(conn, query)

with st.sidebar:
    st.header("Filters")
    df = get_data(mock=use_mock_data)
    df['ORDER_DATE'] = pd.to_datetime(df['ORDER_DATE'])
    min_date, max_date = df['ORDER_DATE'].min(), df['ORDER_DATE'].max()
    date_range = st.date_input("Select Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered_df = df[(df['ORDER_DATE'] >= start_date) & (df['ORDER_DATE'] <= end_date)]
else: filtered_df = df

st.subheader("Key Performance Indicators")
col1, col2, col3 = st.columns(3)
with col1: st.metric(label="💰 Total Revenue", value=f"$${filtered_df['SALES_AMOUNT'].sum():,.2f}")
with col2: st.metric(label="🛍️ Total Orders", value=f"{len(filtered_df):,}")
with col3: st.metric(label="📊 Avg Order Value", value=f"$${filtered_df['SALES_AMOUNT'].mean():,.2f}")
st.divider()
col1, col2 = st.columns(2)
with col1: st.subheader("Sales Trend"); st.plotly_chart(px.line(filtered_df.groupby('ORDER_DATE')['SALES_AMOUNT'].sum().reset_index(), x='ORDER_DATE', y='SALES_AMOUNT', markers=True, color_discrete_sequence=['#29B5E8']), use_container_width=True)
with col2: st.subheader("Sales by Category"); st.plotly_chart(px.donut(filtered_df.groupby('CATEGORY')['SALES_AMOUNT'].sum().reset_index(), values='SALES_AMOUNT', names='CATEGORY', hole=0.4), use_container_width=True)
st.subheader("Recent Orders"); st.dataframe(filtered_df.sort_values(by='ORDER_DATE', ascending=False).head(100), use_container_width=True)

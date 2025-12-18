import streamlit as st
import pandas as pd
import plotly.express as px
from snowflake_connector import init_connection, run_query
import numpy as np

st.set_page_config(page_title="Retail Analytics", layout="wide")
st.title("Executive Retail Dashboard")
st.write("Powered by Snowflake and Streamlit")

if "snowflake" not in st.secrets:
    st.warning("No Snowflake credentials found. Running in Demo Mode.")
    conn = None
else:
    conn = init_connection()
    if conn:
        st.success("Connected to Snowflake")

def get_data():
    # Mock data for stability
    dates = pd.date_range(start="2023-01-01", end="2023-12-31")
    sales = np.random.randint(1000, 5000, size=len(dates))
    categories = np.random.choice(['Electronics', 'Furniture', 'Clothing', 'Books'], size=len(dates))
    return pd.DataFrame({'ORDER_DATE': dates, 'SALES_AMOUNT': sales, 'CATEGORY': categories})

df = get_data()
st.subheader("Key Metrics")
col1, col2 = st.columns(2)
col1.metric("Total Revenue", f"$${df['SALES_AMOUNT'].sum():,.2f}")
col2.metric("Total Orders", len(df))

st.subheader("Sales Trend")
st.plotly_chart(px.line(df.groupby('ORDER_DATE')['SALES_AMOUNT'].sum().reset_index(), x='ORDER_DATE', y='SALES_AMOUNT'))

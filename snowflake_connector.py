import snowflake.connector
import streamlit as st
import pandas as pd

@st.cache_resource
def init_connection():
    try: return snowflake.connector.connect(**st.secrets["snowflake"], client_session_keep_alive=True)
    except: return None

@st.cache_data(ttl=600)
def run_query(_conn, query):
    try:
        cursor = _conn.cursor(); cursor.execute(query); return cursor.fetch_pandas_all()
    except Exception as e: st.error(f"Query error: {e}"); return pd.DataFrame()

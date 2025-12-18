import streamlit as st

def init_connection():
    try:
        import snowflake.connector
        return snowflake.connector.connect(**st.secrets["snowflake"])
    except Exception as e:
        st.error(f"Snowflake Connector Error: {e}")
        return None

def run_query(query):
    try:
        conn = init_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()
    except Exception as e:
        st.error(f"Query Error: {e}")
    return None

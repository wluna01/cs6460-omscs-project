import os
import streamlit as st

def get_credentials():
    # Get the credentials from the environment variables when running locally
    if 'SNOWFLAKE_USER' in os.environ:
        snowflake_user = os.getenv('SNOWFLAKE_USER')
        snowflake_password = os.getenv('SNOWFLAKE_PASSWORD')
        snowflake_account = os.getenv('SNOWFLAKE_ACCOUNT')
    else: # Fallback to Streamlit secrets in production
        snowflake_user = st.secrets["SNOWFLAKE_USER"]
        snowflake_password = st.secrets["SNOWFLAKE_PASSWORD"]
        snowflake_account = st.secrets["SNOWFLAKE_ACCOUNT"]
    return snowflake_user, snowflake_password, snowflake_account

def get_data(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

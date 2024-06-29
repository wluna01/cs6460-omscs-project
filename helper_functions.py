import os
import streamlit as st
import snowflake.connector

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

def get_data(query):
    # Get Snowflake credentials
    snowflake_user, snowflake_password, snowflake_account = get_credentials()

    # Establish connection to Snowflake
    conn = snowflake.connector.connect(
        user=snowflake_user,
        password=snowflake_password,
        account=snowflake_account
    )

    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return result

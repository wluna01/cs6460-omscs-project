import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta 
import nltk
import snowflake.connector
import os

if 'SNOWFLAKE_USER' in os.environ:
    snowflake_user = os.getenv('SNOWFLAKE_USER')
    snowflake_password = os.getenv('SNOWFLAKE_PASSWORD')
    snowflake_account = os.getenv('SNOWFLAKE_ACCOUNT')
else:
    # Fallback to Streamlit secrets in production
    snowflake_user = st.secrets["SNOWFLAKE_USER"]
    snowflake_password = st.secrets["SNOWFLAKE_PASSWORD"]
    snowflake_account = st.secrets["SNOWFLAKE_ACCOUNT"]

def get_data(query):
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# Establish the connection
conn = snowflake.connector.connect(
    user=snowflake_user,
    password=snowflake_password,
    account=snowflake_account
)

story_portions = get_data("SELECT * FROM educational_technology.stories.la_tortuga_gigante LIMIT 10")
st.write(story_portions[0][1])

st.write("Hello, world!")
st.write("Oh Brave New World, that has such people in it! with datetime")

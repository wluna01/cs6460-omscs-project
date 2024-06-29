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

st.write("Hello, world!")
st.write("Oh Brave New World, that has such people in it! with datetime")

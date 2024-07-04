import os
import streamlit as st
import snowflake.connector
from snowflake.connector.pandas_tools import pd_writer
from datetime import datetime, timedelta 
import random
import pandas as pd

def get_credentials():
    """Fetches Snowflake credentials for database authentication.
    Secrets available locally and via Streamlit Cloud.

    Args: None

    Returns:
        tuple: Snowflake credentials (user, password, account)
    """
    
    if 'SNOWFLAKE_USER' in os.environ: # Local development
        snowflake_user = os.getenv('SNOWFLAKE_USER')
        snowflake_password = os.getenv('SNOWFLAKE_PASSWORD')
        snowflake_account = os.getenv('SNOWFLAKE_ACCOUNT')
    else: # Streamlit Cloud
        snowflake_user = st.secrets["SNOWFLAKE_USER"]
        snowflake_password = st.secrets["SNOWFLAKE_PASSWORD"]
        snowflake_account = st.secrets["SNOWFLAKE_ACCOUNT"]
    return snowflake_user, snowflake_password, snowflake_account

def execute_sql(query, returns_results=False):
    """Executes a SQL query on Snowflake with option to returns the results as a pandas DataFrame.

    Args:
        query (str): The SQL query to execute.

    Returns:
        pd.DataFrame: A DataFrame representing the query results.
    """
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
    if returns_results:
        df = cursor.fetch_pandas_all()  # Fetch the query results as a pandas DataFrame

    cursor.close()
    conn.close()

    if returns_results:
        return df


def add_flashcard(word):
    current_time = datetime.now()
    next_review = current_time + timedelta(minutes=1)
    # if the word is already in the table, resets the review time
    user_name = str(st.session_state.user_name)
    sql = f"""
        MERGE INTO educational_technology.mvp_project.flashcards as t 
        USING (select '{user_name}' as user_name, '{word}' as word, 0 as num_consecutive_successful_reviews, '{current_time}' as last_reviewed_at_utc, '{next_review}' as next_review_scheduled_at_utc) as s
        ON t.word = s.word AND t.user_name = s.user_name
        WHEN MATCHED THEN
            UPDATE SET
                t.num_consecutive_successful_reviews = s.num_consecutive_successful_reviews,
                t.last_reviewed_at_utc = s.last_reviewed_at_utc,
                t.next_review_scheduled_at_utc = s.next_review_scheduled_at_utc
        WHEN NOT MATCHED THEN
            INSERT (user_name, word, num_consecutive_successful_reviews, last_reviewed_at_utc, next_review_scheduled_at_utc)
            VALUES (s.user_name, s.word, s.num_consecutive_successful_reviews, s.last_reviewed_at_utc, s.next_review_scheduled_at_utc)
    """
    execute_sql(sql)

def get_review_word():
    user_name = str(st.session_state.user_name)
    sql = f"""select word from educational_technology.mvp_project.flashcards where user_name = '{user_name}' order by next_review_scheduled_at_utc desc"""
    review_word = execute_sql(sql)
    st.session_state.review_word = review_word
    #if review_word.empty == False:
    #    return review_word.iat[0,0]
    #else:
    #    return None

def generate_identifier():
    colors = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Black", "White", "Grey"]
    animals = ["Lion", "Tiger", "Bear", "Kangaroo", "Eagle", "Falcon", "Wolf", "Fox", "Rabbit"]

    color = random.choice(colors)
    animal = random.choice(animals)

    return f"{color}{animal}"

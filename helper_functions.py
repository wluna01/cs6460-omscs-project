import os
import streamlit as st
import snowflake.connector
from datetime import datetime, timedelta 

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

def execute_sql(query):
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
    cursor.close()
    conn.close()


def add_flashcard(word):
    current_time = datetime.now()
    next_review = current_time + timedelta(minutes=1)
    # if the word is already in the table, resets the review time
    sql = f"""
        MERGE INTO educational_technology.vocabulary.wluna as t 
        USING (select '{word}' as word, 0 as num_consecutive_successful_reviews, '{current_time}' as last_reviewed_at_utc, '{next_review}' as next_review_due_at_utc) as s
        ON t.word = s.word
        WHEN MATCHED THEN
            UPDATE SET
                t.num_consecutive_successful_reviews = s.num_consecutive_successful_reviews,
                t.last_reviewed_at_utc = s.last_reviewed_at_utc,
                t.next_review_due_at_utc = s.next_review_due_at_utc
        WHEN NOT MATCHED THEN
            INSERT (word, num_consecutive_successful_reviews, last_reviewed_at_utc, next_review_due_at_utc)
            VALUES (s.word, s.num_consecutive_successful_reviews, s.last_reviewed_at_utc, s.next_review_due_at_utc)
    """
    execute_sql(sql)

def get_review_word():
    sql = f"""select word from educational_technology.vocabulary.wluna order by next_review_due_at_utc desc limit 1"""
    return get_data(sql)[0][0]

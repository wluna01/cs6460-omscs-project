import os
import streamlit as st
import snowflake.connector
from snowflake.connector.pandas_tools import pd_writer
from datetime import datetime, timedelta 
import random

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
# allegedly returns either a list of lists that represents the table
# or an empty list if the query returns no results
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
    #result = cursor.fetchall()
    df = cursor.fetch_pandas_all()
    cursor.close()
    conn.close()

    return df

def load_story(story_name, user_name):
    #"select * from educational_technology.stories.la_tortuga_gigante limit 10

    #get all the rewritten segments of the story, if any, for this user
    query_rewritten_segments = f"""
        select
            story_segment_number,
            story_segment_text
        from educational_technology.mvp_project.rewritten_story_segments
        where story_name = '{story_name}' and user_name = '{user_name}'
    """
    rewritten_segments = get_data(query_rewritten_segments)

    query_original_segments = f"""
        select
            story_segment_number,
            story_segment_text
        from educational_technology.mvp_project.original_story_segments
        where story_name = '{story_name}'
    """
    original_segments = get_data(query_original_segments)

    

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
        MERGE INTO educational_technology.mvp_project.flashcards as t 
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
    sql = f"""select word from educational_technology.mvp_project.flashcards order by next_review_due_at_utc desc limit 1"""
    return get_data(sql)[0][0]

def generate_identifier():
    colors = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Black", "White", "Grey"]
    animals = ["Lion", "Tiger", "Bear", "Kangaroo", "Eagle", "Falcon", "Wolf", "Fox", "Rabbit"]

    color = random.choice(colors)
    animal = random.choice(animals)

    return f"{color}{animal}"

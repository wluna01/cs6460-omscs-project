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

def get_sql(template_file: str, **kwargs) -> str:
    """Reads the SQL query template from the specified file and formats it with the provided arguments.

    Args:
        template_file (str): The name of the file containing the SQL query template.
        **kwargs: Arbitrary keyword arguments to format the query template.

    Returns:
        str: The formatted SQL query.
    """
    with open(template_file, 'r') as file:
        query_template = file.read()
    
    return query_template.format(**kwargs)

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

def add_flashcard(word: str) -> None:
    """Adds a flashcard to the flashcards table.
    
    If the word already exists, it will reset its study progress.

    Args:
        word (str): The word to be inserted or updated.
    """
    current_time = datetime.now()
    next_review = current_time + timedelta(minutes=1)
    user_name = str(st.session_state.user_name)

    sql = get_sql("sql_queries/add_flashcard.sql", user_name=user_name, word=word, current_time=current_time, next_review=next_review)
    execute_sql(sql)

def get_review_word() -> None:
    """Fetches a word for review from the flashcards table and stores it in the session state.
    
    The function retrieves a word that is due for review for the current user and stores it in the session state.
    """
    user_name = str(st.session_state.user_name)
    sql = get_sql("sql_queries/get_review_word.sql", user_name=user_name)
    review_word = execute_sql(sql, returns_results=True)
    st.session_state.review_word = review_word
    #if review_word.empty == False:
    #    return review_word.iat[0,0]
    #else:
    #    return None

def generate_identifier() -> str:
    """Generates a unique identifier consisting of a random color and animal.
    
    The function randomly selects a color from a predefined list of colors and an animal
    from a predefined list of animals, and combines them to create a unique identifier.
    
    Returns:
        str: A unique identifier in the format "ColorAnimal".
    """
    colors = ["Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Black", "White", "Grey"]
    animals = ["Lion", "Tiger", "Bear", "Kangaroo", "Eagle", "Falcon", "Wolf", "Fox", "Rabbit"]

    color = random.choice(colors)
    animal = random.choice(animals)

    return f"{color}{animal}"

def story_available(story_name: str) -> bool:
    """Checks if a story is available in the stories table.

    Args:
        story_name (str): The name of the story to check.

    Returns:
        bool: True if the story is available, False otherwise.
    """
    sql = get_sql("sql_queries/story_available.sql", story_name=story_name)
    story = execute_sql(sql, returns_results=True)
    return not story.empty

def user_started_story(user_name: str, story_name: str) -> bool:
    """Checks if a user has started reading a story.

    Args:
        user_name (str): The name of the user.
        story_name (str): The name of the story.

    Returns:
        bool: True if the user has started reading the story, False otherwise.
    """
    sql = get_sql("sql_queries/user_started_story.sql", user_name=user_name, story_name=story_name)
    user_story = execute_sql(sql, returns_results=True)
    return not user_story.empty

def start_story(user_name: str, story_name: str) -> None:
    """Writes the first original segment of a story to the user stories table.

    Args:
        user_name (str): The name of the user.
        story_name (str): The name of the story.
    """
    sql = get_sql("sql_queries/get_first_story_segment.sql", story_name=story_name)
    first_story_segment_df = execute_sql(sql, returns_results=True)
    first_story_segment = first_story_segment_df.iat[0,0]
    sql = get_sql("sql_queries/insert_user_story_segment.sql", user_name=user_name, story_name=story_name, story_segment_number=1, story_segment_text=first_story_segment)
    execute_sql(sql)

def get_read_segments(user_name: str, story_name: str) -> pd.DataFrame:
    """Fetches the story read thus far for a given user and story name.

    Args:
        user_name (str): The name of the user.
        story_name (str): The name of the story.
    
    Returns:
        story_segments (pd.DataFrame) A DataFrame containing the story segments read by the user.
    """
    sql = get_sql("sql_queries/get_read_user_story_segments.sql", user_name=user_name, story_name=story_name)
    story_segments = execute_sql(sql, returns_results=True)
    return story_segments

def get_story_segments(user_name: str, story_name: str) -> pd.DataFrame:
    """Fetches the story read thus far for a given user and story name.

    Args:
        user_name (str): The name of the user.
        story_name (str): The name of the story.
    
    Returns:
        story_segments (pd.DataFrame) A DataFrame containing the story segments read by the user.
    """

    if story_available(story_name) == False:
        raise Exception(f"Story '{story_name}' is not available.")
    
    # if the user has not started reading the story
    if user_started_story(user_name, story_name) == False:
        # write the first original segment to the user stories table
        start_story(user_name, story_name)

    # get all segments read thus far
    story_segments = get_read_segments(user_name, story_name)
    return story_segments

def update_vocabulary_model() -> None:
    """Updates the flashcard list with all words from the most recently read segment
    """
    # sets the latest segment read to the row in the story segments dataframe with the highest story_segment_number
    latest_segment = st.session_state.story.story_segments.loc[st.session_state.story.story_segments['STORY_SEGMENT_NUMBER'].idxmax()]['STORY_SEGMENT_TEXT']
    words = latest_segment.split()
    for word in words:
        if already_in_flashcards(word) == True:
            add_successful_review(word)
        else:
            add_flashcard(word, longterm_memory=True)

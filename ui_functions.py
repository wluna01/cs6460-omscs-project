from helper_functions import execute_sql, add_flashcard, update_vocabulary_model, add_story_segment
import streamlit as st

def on_click_continue():
    update_vocabulary_model()
    add_story_segment()

def on_click_dictionary_lookup(word):
    if word:
        source_language = "es"
        target_language = "en"
        query = f"""select snowflake.cortex.translate('{word}', '{source_language}', '{target_language}') as translation"""
        translation = execute_sql(query, returns_results=True)
        add_flashcard(word)
        st.session_state.definition = translation.iat[0, 0]
    else:
        st.session_state.definition = ""

def convert_to_title(text):
    """Converts a variable name to a title format.
    Replaces underscores with spaces and capitalizes the first letter of each word.
    """
    return text.replace("_", " ").title()

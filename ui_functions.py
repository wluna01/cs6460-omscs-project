from helper_functions import get_data, add_flashcard
import streamlit as st

def on_click_continue():
    st.session_state.story.num_segments_displayed += 1

def on_click_dictionary_lookup(word):
    if word:
        source_language = "es"
        target_language = "en"
        query = f"""select snowflake.cortex.translate('{word}', '{source_language}', '{target_language}')"""
        translation = get_data(query)
        add_flashcard(word)
        st.session_state.definition = translation[0][0]
    else:
        st.session_state.definition = ""

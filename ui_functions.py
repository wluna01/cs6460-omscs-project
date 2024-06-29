from helper_functions import get_data, add_flashcard, get_review_word
import streamlit as st

def on_click_continue():
    #get the next flashcard to study
    review_word = get_review_word()
    st.session_state.review_word = review_word
    text = st.session_state.story.segments[st.session_state.story.num_segments_displayed][1]
    prompt = f"""Please rewrite a story excerpt. Your rewrite should include at least one instance of the word: {review_word}. Do not preface your response in any way, only include the rewritten passage, and rewrite the passage in the original language of the text. The excerpt is: {text}"""
    query = f"""select snowflake.cortex.complete('llama3-70b', '{prompt}')"""
    response = get_data(query)
    #st.session_state.test_response = "some response change"
    st.session_state.test_response = response[0][0]

def on_click_dictionary_lookup(word):
    if word:
        source_language = "es"
        target_language = "en"
        query = f"""select snowflake.cortex.translate('{word}', '{source_language}', '{target_language}') as translation"""
        translation = get_data(query)
        add_flashcard(word)
        st.session_state.definition = translation.iat[0, 0]
    else:
        st.session_state.definition = ""

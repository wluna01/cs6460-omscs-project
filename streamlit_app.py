import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import nltk
from ui_functions import on_click_continue, on_click_dictionary_lookup
from helper_functions import generate_identifier
from story import Story
from text_to_speech import text_to_speech

st.session_state.story_name = st.text_input(label="Story Name (cannot change during demo)", value="la_tortuga_gigante", max_chars=20)
if "user_name" not in st.session_state:
    st.session_state.user_name = st.text_input(label="User Name (randomly generated during demo. data persists for those already used)", value=generate_identifier(), max_chars=20)
else:
    st.session_state.user_name = st.text_input(label="User Name (randomly generated during demo. data persists for those already used)", value=st.session_state.user_name, max_chars=20)

audio_is_on = st.toggle("Audio", True)

st.title("The Giant Tortoise")

# create instance of the story class
if "story" not in st.session_state:
    st.session_state.story = Story()

# Display segments
for index, row in st.session_state.story.segments.iterrows():
    if index < st.session_state.story.num_segments_displayed:
        st.write(index+1)
        if audio_is_on:
            audio_file = text_to_speech(row['STORY_SEGMENT_TEXT'])
            audio_bytes = open(audio_file, 'rb').read()
            st.audio(audio_bytes, format='audio/mp3', autoplay=True)
        st.write(row['STORY_SEGMENT_TEXT'])

if st.session_state.story.num_segments_displayed < st.session_state.story.total_number_of_segments:
    st.button("Continue", on_click=on_click_continue)
else:
    st.title("The End")

word_to_lookup = st.text_input("Dictionary :thinking_face:", max_chars=20)
st.button("Search", on_click=on_click_dictionary_lookup(word_to_lookup))
definition_text = st.text(st.session_state.definition)

with st.expander("Diagnostics"):
    st.text("# Segments Displayed: " + str(st.session_state.story.num_segments_displayed))
    st.text("# Total Segments: " + str(st.session_state.story.total_number_of_segments))
    if "review_word" in st.session_state:
        st.write("Review DF is: ")
        st.dataframe(st.session_state.review_word)
    st.write("All Segments:")
    st.dataframe(st.session_state.story.segments)

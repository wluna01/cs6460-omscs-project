import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import nltk
from ui_functions import on_click_continue, on_click_dictionary_lookup
from helper_functions import generate_identifier
from story import Story
from text_to_speech import text_to_speech
from ui_components import show_sidebar, show_highlightable_passage

st.session_state.story_name = st.text_input(label="Story Name (cannot change during demo)", value="la_tortuga_gigante", max_chars=20)
if "user_name" not in st.session_state:
    st.session_state.user_name = st.text_input(label="User Name (randomly generated during demo. data persists for those already used)", value=generate_identifier(), max_chars=20)
else:
    st.session_state.user_name = st.text_input(label="User Name (randomly generated during demo. data persists for those already used)", value=st.session_state.user_name, max_chars=20)

st.title("The Giant Tortoise")
play_icon = "▶️"
# create instance of the story class
if "story" not in st.session_state:
    st.session_state.story = Story()

#auto play toggle set to off by default
auto_play = st.toggle("Auto Play Audio", value=False)

# Display segments
for index, row in st.session_state.story.segments.iterrows():
    if index < st.session_state.story.num_segments_displayed:
        st.write(index+1)
        #st.write(row['STORY_SEGMENT_TEXT'])
        show_highlightable_passage(row['STORY_SEGMENT_TEXT'])
        play_this = st.button(play_icon)
        #if the play button was clicked or auto play is on and this is the last segment
        if play_this or (auto_play and index == st.session_state.story.num_segments_displayed-1):
            #generate and play the audio
            audio_file = text_to_speech(row['STORY_SEGMENT_TEXT'])
            audio_bytes = open(audio_file, 'rb').read()
            st.audio(audio_bytes, format='audio/mp3', autoplay=True)

if st.session_state.story.num_segments_displayed < st.session_state.story.total_number_of_segments:
    st.button("Continue", on_click=on_click_continue)
else:
    st.title("The End")

word_to_lookup = st.text_input("Dictionary :thinking_face:", max_chars=20)
st.button("Search", on_click=on_click_dictionary_lookup(word_to_lookup))
definition_text = st.text(st.session_state.definition)

show_sidebar()

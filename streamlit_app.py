import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import nltk
from ui_functions import on_click_continue, on_click_dictionary_lookup
from helper_functions import generate_identifier
from story import Story
from text_to_speech import play_audio
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

#show_sidebar()

# Display segments
for index, row in st.session_state.story.story_segments.iterrows():
    play_this = st.button(play_icon)
    show_highlightable_passage(row['STORY_SEGMENT_TEXT'])
    if play_this: # or (st.session_state.auto_play and index == st.session_state.story.num_segments_displayed-1):
        play_audio(row['STORY_SEGMENT_TEXT'])

    #if index < st.session_state.story.num_segments_displayed:
        #st.write(index+1)
        #st.write(row['STORY_SEGMENT_TEXT'])
        #play_this = st.button(play_icon)
        
        #if the play button was clicked or auto play is on and this is the last segment
        #if play_this or (st.session_state.auto_play and index == st.session_state.story.num_segments_displayed-1):
        #    play_audio(row['STORY_SEGMENT_TEXT'])

st.button("Continue", on_click=on_click_continue)

word_to_lookup = st.text_input("Dictionary :thinking_face:", max_chars=20)
st.button("Search", on_click=on_click_dictionary_lookup(word_to_lookup))
definition_text = st.text(st.session_state.definition)

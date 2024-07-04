import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import nltk
from ui_functions import on_click_continue, on_click_dictionary_lookup
from helper_functions import generate_identifier
from story import Story
from ui_components import show_sidebar, show_highlightable_passage, show_dictionary, show_segments, show_title, show_continue

st.session_state.story_name = st.text_input(label="Story Name (cannot change during demo)", value="la_tortuga_gigante", max_chars=20)
if "user_name" not in st.session_state:
    st.session_state.user_name = st.text_input(label="User Name (randomly generated during demo. data persists for those already used)", value=generate_identifier(), max_chars=20)
else:
    st.session_state.user_name = st.text_input(label="User Name (randomly generated during demo. data persists for those already used)", value=st.session_state.user_name, max_chars=20)

show_title()
# create instance of the story class
#if "story" not in st.session_state:
st.session_state.story = Story()

#show_sidebar()

show_segments()

show_continue()

show_dictionary()

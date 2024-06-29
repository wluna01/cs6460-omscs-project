import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta 
import nltk
from ui_functions import on_click_continue, on_click_dictionary_lookup
from story import Story

st.title("La Tortuga Gigante")

# create instance of the story class
if "story" not in st.session_state:
    st.session_state.story = Story()

# Display segments
for i in range(0, st.session_state.story.num_segments_displayed):
    st.write(st.session_state.story.segments[i][0])
    st.write(st.session_state.story.segments[i][1])

if st.session_state.story.num_segments_displayed < st.session_state.story.total_number_of_segments:
    st.button("Continuar", on_click=on_click_continue)
else:
    st.title("Fin")

word_to_lookup = st.text_input("Palabra Desconocida :thinking_face:", max_chars=20)
st.button("Buscar", on_click=on_click_dictionary_lookup(word_to_lookup))
definition_text = st.text(st.session_state.definition)

st.title("Diagnostics")
st.write("# Segments Displayed: " + str(st.session_state.story.num_segments_displayed))
st.write("# Total Segments: " + str(st.session_state.story.total_number_of_segments))
#st.write(story.segments[0][1])

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import nltk
from ui_functions import on_click_continue, on_click_dictionary_lookup
from helper_functions import generate_identifier
from story import Story

st.session_state.story_name = st.text_input(label="Story Name (cannot change during demo)", value="la_tortuga_gigante", max_chars=20)
st.session_state.user_name = st.text_input(label="User Name (randomly generated during demo)", value=generate_identifier(), max_chars=20)

#testing only
if "review_word" not in st.session_state:
    st.session_state.review_word = "nothing yet"
if "test_response" not in st.session_state:
    st.session_state.test_response = "nothing yet"

st.title("La Tortuga Gigante")

# create instance of the story class
if "story" not in st.session_state:
    st.session_state.story = Story()

# Display segments
#st.dataframe(st.session_state.story.segments)
for index, row in st.session_state.story.segments.iterrows():
    st.write(row['STORY_SEGMENT_NUMBER'])
    st.write(row['STORY_SEGMENT_TEXT'])

#for i in range(0, st.session_state.story.num_segments_displayed):
    #st.write(st.session_state.story.segments[i][0])
    #st.write(st.session_state.story.segments[i][1])

if st.session_state.story.num_segments_displayed < st.session_state.story.total_number_of_segments:
    st.button("Continuar", on_click=on_click_continue)
else:
    st.title("Fin")

word_to_lookup = st.text_input("Palabra Desconocida :thinking_face:", max_chars=20)
st.button("Buscar", on_click=on_click_dictionary_lookup(word_to_lookup))
definition_text = st.text(st.session_state.definition)

with st.expander("Diagnostics"):
    st.write("# Segments Displayed: " + str(st.session_state.story.num_segments_displayed))
    st.write("# Total Segments: " + str(st.session_state.story.total_number_of_segments))
    st.write("Word to Incorporate in Re-written segment: " + str(st.session_state.review_word))
    st.write("Re-written Segment: " + str(st.session_state.test_response))

#st.write(story.segments[0][1])

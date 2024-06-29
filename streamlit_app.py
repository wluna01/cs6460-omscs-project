import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta 
import nltk
import snowflake.connector
import os
from helper_functions import get_data, get_credentials
from story import Story

def on_click_continue():
    #if story.num_segments_displayed < story.total_number_of_segments:
    st.session_state.story.num_segments_displayed += 1

# Get Snowflake credentials
snowflake_user, snowflake_password, snowflake_account = get_credentials()

# Establish connection to Snowflake
conn = snowflake.connector.connect(
    user=snowflake_user,
    password=snowflake_password,
    account=snowflake_account
)

st.title("La Tortuga Gigante")

# create instance of the story class
if "story" not in st.session_state:
    st.session_state.story = Story()
    st.session_state.story.segments = get_data(conn, "select * from educational_technology.stories.la_tortuga_gigante limit 10")
    st.session_state.story.total_number_of_segments = len(st.session_state.story.segments)
    st.session_state.story.num_segments_displayed += 1

# Display segments
for i in range(0, st.session_state.story.num_segments_displayed):
    st.write(st.session_state.story.segments[i][0])
    st.write(st.session_state.story.segments[i][1])

if st.session_state.story.num_segments_displayed < st.session_state.story.total_number_of_segments:
    st.button("Continuar", on_click=on_click_continue)
else:
    st.title("Fin")

st.title("Diagnostics")
st.write("# Segments Displayed: " + str(st.session_state.story.num_segments_displayed))
st.write("# Total Segments: " + str(st.session_state.story.total_number_of_segments))
#st.write(story.segments[0][1])

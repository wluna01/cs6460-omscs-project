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
story = Story()
if story.has_pulled_segments == False:
    story.segments = get_data(conn, "select * from educational_technology.stories.la_tortuga_gigante limit 10")
    story.has_pulled_segments = True
    story.total_number_of_segments = len(story.segments)

#story_portions = get_data(conn, "select * from educational_technology.stories.la_tortuga_gigante limit 10")
st.write(story.segments[0][1])

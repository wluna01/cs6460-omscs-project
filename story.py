'''
Defines the story class that will hold the story data and manage the story's state.
'''
import streamlit as st
from helper_functions import get_story_segments

class Story:
    """
    A class to represent a story, managing its segments and state for a user.

    Attributes:
        story_name (str): The name of the story from the session state.
        user_name (str): The name of the user from the session state.
        segments (DataFrame): DataFrame containing the story segments.
        num_segments_displayed (int): Number of segments read by the user.
        total_number_of_segments (int): Total number of segments in the story.
    """

    def __init__(self):
        #self.story_name = st.session_state.story_name
        #self.user_name = st.session_state.user_name

        self.story_segments = get_story_segments(st.session_state.user_name, st.session_state.story_name)
        self.num_segments_displayed = len(self.story_segments)

'''
Defines the story class that will hold the story data and manage the story's state.
'''
import streamlit as st
from helper_functions import execute_sql, get_story_segments

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
        '''
        story_segments_query = f"""
            select
                o.story_segment_number,
                coalesce(r.story_segment_text, o.story_segment_text) as story_segment_text
            from educational_technology.mvp_project.original_story_segments as o
            left join educational_technology.mvp_project.rewritten_story_segments as r
                on o.story_segment_number = r.story_segment_number
                and r.story_name = '{self.story_name}'
                and r.user_name = '{self.user_name}'
            where o.story_name = '{self.story_name}'
            order by o.story_segment_number asc
        """
        self.segments = execute_sql(story_segments_query, returns_results=True)
        number_segments_read_query = f"""
            select max(story_segment_number) as num_segments_read
            from educational_technology.mvp_project.rewritten_story_segments
            where story_name = '{self.story_name}'
                and user_name = '{self.user_name}'
        """
        number_segments_read = execute_sql(number_segments_read_query, returns_results=True)
        if number_segments_read.empty:
            self.num_segments_displayed = number_segments_read[0][0]
        else:
            self.num_segments_displayed = 1
        self.total_number_of_segments = len(self.segments)
        '''

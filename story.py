'''
Defines the story class that will hold the story data and manage the story's state.
'''
import streamlit as st
from helper_functions import get_data
#defines story class
class Story:
    def __init__(self):
        self.story_name = st.session_state.story_name
        self.user_name = st.session_state.user_name
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
        self.segments = get_data(story_segments_query)
        #self.segments = load_story(self.story_name, self.user_name)
        number_segments_read_query = f"""
            select max(story_segment_number) as num_segments_read
            from educational_technology.mvp_project.rewritten_story_segments
            where story_name = '{self.story_name}'
                and user_name = '{self.user_name}'
        """
        number_segments_read = get_data(number_segments_read_query)
        if number_segments_read.empty:
            self.num_segments_displayed = number_segments_read[0][0]
        else:
            self.num_segments_displayed = 1
        self.total_number_of_segments = len(self.segments)

import streamlit as st

def on_click_continue():
    st.session_state.story.num_segments_displayed += 1

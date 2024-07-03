import streamlit as st

def show_sidebar():
    with st.sidebar:
        st.title("Settings")
        with st.expander("Diagnostics"):
            st.text("# Segments Displayed: " + str(st.session_state.story.num_segments_displayed))
            st.text("# Total Segments: " + str(st.session_state.story.total_number_of_segments))
            if "review_word" in st.session_state:
                st.write("Review DF is: ")
                st.dataframe(st.session_state.review_word)
            st.write("All Segments:")
            st.dataframe(st.session_state.story.segments)

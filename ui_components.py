import streamlit as st
import streamlit.components.v1 as components

def show_sidebar():
    with st.sidebar:
        st.title("Settings")
        auto_play = st.toggle("Auto Play Audio", value=False) # off by default
        st.session_state.auto_play = auto_play
        with st.expander("Diagnostics"):
            st.text("# Segments Displayed: " + str(st.session_state.story.num_segments_displayed))
            st.text("# Total Segments: " + str(st.session_state.story.total_number_of_segments))
            if "review_word" in st.session_state:
                st.write("Review DF is: ")
                st.dataframe(st.session_state.review_word)
            st.write("All Segments:")
            st.dataframe(st.session_state.story.segments)

# Function to generate HTML and JavaScript for word interaction
def generate_text_with_js(text):
    words = text.split()
    html_words = ' '.join([f'<span class="hoverable">{word}</span>' for word in words])
    custom_html = f"""
    <html>
    <head>
        <style>
            .hoverable {{
                cursor: pointer;
                display: inline-block;
                color: black;
            }}
            .hoverable:hover {{
                background-color: yellow;
            }}
        </style>
    </head>
    <body>
        <div>{html_words}</div>
    </body>
    </html>
    """
    return custom_html

# Function to display a highlightable passage
def show_highlightable_passage(text):
    html_content = generate_text_with_js(text)
    components.html(html_content, height=200)

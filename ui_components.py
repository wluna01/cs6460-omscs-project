import streamlit as st
import streamlit.components.v1 as components
from streamlit_annotation_tools import text_highlighter
from ui_functions import on_click_dictionary_lookup, convert_to_title, on_click_continue
from text_to_speech import play_audio

def show_title():
    st.title(convert_to_title(st.session_state.story_name))
 
def show_segments():
    play_icon = "▶️"
    for index, row in st.session_state.story.story_segments.iterrows():
        play_this = st.button(play_icon)
        annotations = text_highlighter(row['STORY_SEGMENT_TEXT'])
        if annotations is not None:
            #for annotation in annotations[0]:
            st.write(str(annotation["label"] + " ") for annotation in annotations[0])
        #show_highlightable_passage(row['STORY_SEGMENT_TEXT'])
        if play_this:
            play_audio(row['STORY_SEGMENT_TEXT'])

def show_continue():
    st.button("Continue", on_click=on_click_continue)

def show_sidebar():
    with st.sidebar:
        st.title("Settings")
        auto_play = st.toggle("Auto Play Audio", value=False) # off by default
        st.session_state.auto_play = auto_play
        with st.expander("Diagnostics"):
            st.text("# Segments Read: " + str(st.session_state.story.num_segments_displayed))
            if "review_word" in st.session_state:
                st.write("Review DF is: ")
                st.dataframe(st.session_state.review_word)
            st.write("All Segments:")
            st.dataframe(st.session_state.story.segments)

def show_dictionary():
    word_to_lookup = st.text_input("Dictionary :thinking_face:", max_chars=20)
    st.button("Search", on_click=on_click_dictionary_lookup(word_to_lookup))
    definition_text = st.text(st.session_state.definition)

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
    components.html(html_content, height=100)

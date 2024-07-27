import streamlit as st
from streamlit_annotation_tools import text_highlighter
from ui_functions import convert_to_title, on_click_continue
from helper_functions import generate_identifier
from text_to_speech import play_audio
from dictionary_functions import get_definition
from story import Story

def define_user_info():
    st.session_state.story_name = st.selectbox(label="Story Name", options=["la_sombra_del_viento", "alice_in_wonderland", "la_tortuga_gigante"])
    if "user_name" not in st.session_state:
        st.session_state.user_name = st.text_input(label="User Name", value=generate_identifier(), max_chars=20)
    else:
        st.session_state.user_name = st.text_input(label="User Name", value=st.session_state.user_name, max_chars=20)
    st.session_state.story = Story()

def show_title():
    st.title(convert_to_title(st.session_state.story_name))

def show_annotated_passage(text : str):
    """Displays a passage of text with words that can be clicked on to get definitions.
    Args: String of text to display
    Returns: If any words are clicked, a list of the clicked words is returned.
        Otherwise an empty list is returned
    """
    annotations = text_highlighter(text)

    if annotations is not None:
        clicked_words = [annotation["label"] for annotation in annotations[0]]
        if len(clicked_words) > 0:
            st.session_state.unknown_words = clicked_words
            show_dictionary()

def show_segments():

    for index, row in st.session_state.story.story_segments.iterrows():

        # make annotations and audio available for the last section only
        if index == st.session_state.story.num_segments_displayed - 1:

            show_annotated_passage(row['STORY_SEGMENT_TEXT'])
        
            play_icon = "▶️"
            play_this = st.button(play_icon + ' Play Audio')
            if play_this or st.session_state.auto_play:
                play_audio(row['STORY_SEGMENT_TEXT'])

        # otherwise just display the text
        else:
            st.write(row['STORY_SEGMENT_TEXT'])

def show_continue():
    st.button("Continue", on_click=on_click_continue)

def show_settings():
    with st.sidebar:
        st.title("Settings")
        define_user_info()
        auto_play = st.toggle("Auto Play Audio", value=False)
        st.session_state.auto_play = auto_play
        st.subheader("Instructions")
        st.caption("Currently only works for Spanish and English. If you want to see how the app works in English, change the story to Alice in Wonderland above.")
        st.caption("Drag your cursor over a word to see its definition below.")
        st.caption("As you look up unknown words, the application builds a model of your vocabulary. Subsequent passages of text will be rewritten to cater to your current language level with unknown words added in to cement them in your long-term memory.")
        st.caption("Please be patient! The app is still in development and may be slow to load.")
        st.caption("The red plus (+) button does not do anything.")
        st.caption("After looking up a word, it will appear in a red box above the text. Please click the 'x' to make that box disappear before looking up another word–this will make the dictionary run much faster.")
        
def show_dictionary():
    with st.sidebar:
        st.title("Dictionary")
        if "unknown_words" in st.session_state:
            for word in st.session_state.unknown_words:
                st.subheader(str(word))
                st.text(get_definition(word))

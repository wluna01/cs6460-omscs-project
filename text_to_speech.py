import streamlit as st
from gtts import gTTS
import os

# Function to convert text to speech
def text_to_speech(text, lang='es'):
    tts = gTTS(text, lang=lang)
    tts.save("output.mp3")
    return "output.mp3"

# Streamlit app
st.title("Text-to-Speech with Streamlit")

text = "A veces la vaca de mi gente no come a la frontera."


# Display the text
st.text(text)

# Button to read text aloud
if st.button("Read Aloud"):
    audio_file = text_to_speech(text)
    audio_bytes = open(audio_file, 'rb').read()
    st.audio(audio_bytes, format='audio/mp3', autoplay=True)

    # Clean up the audio file after playing
    os.remove("output.mp3")

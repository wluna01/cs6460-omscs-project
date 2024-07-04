import streamlit as st
from gtts import gTTS
import os

# Function to convert text to speech
def text_to_speech(text: str, lang="es") -> None:
    tts = gTTS(text, lang=lang)
    tts.save("output.mp3")

def play_audio(text: str) -> None:
    text_to_speech(text)
    audio_bytes = open("output.mp3", "rb").read()
    st.audio(audio_bytes, format="audio/mp3", autoplay=True)
    os.remove("output.mp3")

import streamlit as st
from gtts import gTTS
import os
from google.cloud import texttospeech
# Function to convert text to speech
def text_to_speech__deprecated(text: str, lang="es") -> None:
    tts = gTTS(text, lang=lang)
    tts.save("output.mp3")

def text_to_speech(text, language_code="es-US", voice_name="es-US-Neural2-A", audio_encoding="MP3", output_file="output.mp3"):

    api_key = os.getenv("gcp_tts_api_key")

    client_options = {"api_key": api_key}
    client = texttospeech.TextToSpeechClient(client_options=client_options)

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Save the audio content to a file
    with open(output_file, "wb") as out:
        out.write(response.audio_content)

@st.experimental_fragment
def play_audio(text: str) -> None:
    text_to_speech(text)
    audio_bytes = open("output.mp3", "rb").read()
    st.audio(audio_bytes, format="audio/mp3", autoplay=True)
    #os.remove("output.mp3") probably content to let subsequent plays overwrite the file

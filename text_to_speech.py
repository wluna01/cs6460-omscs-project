import streamlit as st
from google.cloud import texttospeech

def get_tts_credentials() -> str:
    """Fetches Google Cloud credentials for text-to-speech API authentication.
    Secrets available locally and via Streamlit Cloud.

    Args: None

    Returns:
        str: Google Cloud API key
    """
    return st.secrets["GCP_TTS_API_KEY"]

# Function to convert text to speech
@st.experimental_fragment
def text_to_speech(text, language_code, voice_name, audio_encoding="MP3", output_file="output.mp3"):

    api_key = get_tts_credentials()

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
    #this if else is a hack to invoke the right language code.
    #stories should be tagged with their language and fetched in db
    if st.session_state.story_name == "alice_in_wonderland":
        text_to_speech(text, language_code="en-US", voice_name="en-US-Neural2-C")
    else:
        text_to_speech(text, language_code="es-US", voice_name="es-US-Neural2-A")
    audio_bytes = open("output.mp3", "rb").read()
    st.audio(audio_bytes, format="audio/mp3", autoplay=True)
    #os.remove("output.mp3") probably content to let subsequent plays overwrite the file

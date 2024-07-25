import requests
import os
from helper_functions import add_flashcard
import stanza
import streamlit as st
stanza.download('es')
stanza.download('en')

def get_merriam_webster_credentials() -> str:
    """Fetches Merriam-Webster credentials for dictionary API authentication.
    Secrets available locally and via Streamlit Cloud.

    Args: None

    Returns:
        str: Merriam-Webster API key
    """
    return st.secrets["MERRIAM_WEBSTER_API_KEY"]

def get_response(word : str) -> list:
    """Retrieves the English translation of a Spanish word
        or the Spanish translation of an English word
        from the Merriam-Webster Spanish-English dictionary API.
    
    Args: a word in Spanish or English

    Returns: a list of English or Spanish definitions.
        Definitions will be in the language of the word not provided.
    """
    api_key = get_merriam_webster_credentials()
    url = f"https://www.dictionaryapi.com/api/v3/references/spanish/json/{word}?key={api_key}"
    response = requests.get(url).json()
    try:
        definition = response[0]['shortdef']
        return definition
    except:
        return None

def get_lemma(word : str) -> str:
    """Gets the lemma of a Spanish word using the stanza library.

    Args: a word in Spanish

    Returns: the lemma of the same word
    """
    if st.session_state.story_name == "alice_in_wonderland":
        nlp = stanza.Pipeline('en')
    else:
        nlp = stanza.Pipeline('es')
    doc = nlp(word)
    lemma = doc.sentences[0].words[0].lemma
    return lemma

def get_definition(word):
    """Gets the definition of a Spanish word from the Merriam-Webster Spanish-English dictionary API.

    Args: a word in Spanish 

    Returns: a list of English definitions
    """
    definition = get_response(word)
    #first try to get the definition without lemmatizing
    if definition:
        add_flashcard(word)
        return definition
    #if no definition is found, try to get the definition of the lemma
    else:
        lemma = get_lemma(word)
        definition = get_response(lemma)
        if definition:
            add_flashcard(lemma) # add lemma as flashcard
            return definition # then return the definition
        # otherwise return that no definition was found
        else:
            return "No definition found."
    
    '''
    # if the word's definition is found
    if definition:
        lemma = get_lemma(word)
        if lemma:
            add_flashcard(lemma) # add lemma as flashcard
        return definition # then return the definition
    
    # otherwise
    else:
        lemma = get_lemma(word) # take the definition of the lemma
        definition = get_response(lemma) 
        if definition: # if lemma definition is found
            add_flashcard(lemma) # add lemma as flashcard
            return definition # return definition of the lemma
        
        # otherwise return that no definition was found
        else:
            return "No definition found."
    '''

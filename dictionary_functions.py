import requests
import os
from helper_functions import add_flashcard
import stanza
stanza.download('es')

def get_response(word : str) -> str:
    api_key = os.getenv("MERRIAM_WEBSTER_API_KEY")
    url = f"https://www.dictionaryapi.com/api/v3/references/spanish/json/{word}?key={api_key}"
    response = requests.get(url).json()
    try:
        definition = response[0]['shortdef']
        return definition
    except:
        return None

def get_lemma(word):
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

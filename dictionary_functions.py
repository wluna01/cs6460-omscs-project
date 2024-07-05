import requests
import os

def get_definition(word):
    """Gets the definition of a Spanish word from the Merriam-Webster Spanish-English dictionary API."""
    api_key = os.getenv("MERRIAM_WEBSTER_API_KEY")
    url = f"https://www.dictionaryapi.com/api/v3/references/spanish/json/{word}?key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        definition = response.json()[0]['shortdef']
        return definition
    else:
        return "No definition found."

print(get_definition("tortuga"))

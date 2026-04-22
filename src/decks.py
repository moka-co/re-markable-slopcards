import requests
import logging

logger = logging.getLogger(__name__)

ENDPOINT = "http://127.0.0.1:8765"  # AnkiConnect works only locally


# Connect to AnkiConnect API and return all Deck Names
def get_deck_names_and_ids() -> str | None:
    payload = {
        "action": "deckNamesAndIds",
        "version": 6,
    }

    response = requests.post(ENDPOINT, json=payload)
    if response.status_code:  # OK
        body = response.json()
        result = body["result"]
        return result
    else:
        print(f"Request returned status code {response.status_code}")
        return None

def create_deck(deck_name : str) -> str | None:
    payload = {
        "action": "createDeck",
        "version": 6,
        "params" : {
            "deck" : deck_name
        }
    }

    response = requests.post(ENDPOINT, json=payload)
    if response.status_code:  # OK
        body = response.json()
        result = body["result"]
        return result
    else:
        print(f"Request returned status code {response.status_code}")
        return None
    

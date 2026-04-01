from scripts.add_note import add_note
import requests
import re
import csv
import argparse

endpoint="http://127.0.0.1:8765"

# Connect to AnkiConnect API and get all Deck Names
def get_deck_names_and_ids() -> str:
    payload = {
        "action": "deckNamesAndIds",
        "version": 6,
    }

    response = requests.post(endpoint, json=payload)
    if response.status_code: #OK
        body = response.json()
        result = body["result"]
        return result
    else:
        print(f"Request returned status code {response.status_code}")


def add_notes_from_csv_file(file_name, deck_name):
    model_name="Cloze" # By default gemini generates flashcards with cloze
    with open(file_name, newline="") as f:
        reader = csv.reader(f)
        
        # Iterate over each row in the file
        for row in reader:
            front_content = row[0]
            back_content = row[1]

            # Dynamically adapt the model_name
            pattern = r"c1::*"
            if not re.search(pattern, front_content):
                model_name = "Basic"
            else: 
                model_name = "Cloze"

            # Add note 
            add_note(
                deck_name,
                model_name,
                front_content,
                back_content
            )


def get_cards_id_by_deckname(deck_name : str):
    payload= {
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": f'deck:"{deck_name}"'
        }
    }

    print(payload)

    response = requests.post(endpoint, json=payload)
    body = response.json()
    return body['result']

def get_cards_id_by_query(query : str):
    payload= {
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": f'"{query}"'
        }
    }

    response = requests.post(endpoint, json=payload)
    body = response.json()
    return body['result']

def get_notes_info_by_id(note_ids : list):
    payload = {
        "action": "notesInfo",
        "version": 6,
        "params": {
            "notes": note_ids
        }
    }
    response = requests.post(endpoint, json=payload)
    body= response.json()
    return body['result']

def update_note(note_id: int, front: str = None, back: str = None, tags: list = None):
    # Construct the fields dynamically based on what is provided
    fields = {}
    if front:
        fields["Text"] = front
    if back:
        fields["Back Extra"] = back

    payload = {
        "action": "updateNote",
        "version": 6,
        "params": {
            "note": {
                "id": note_id,
                "fields": fields
            }
        }
    }
    
    if tags:
        payload["params"]["note"]["tags"] = tags

    response = requests.post(endpoint, json=payload)
    return response.json()

 
def main() -> None:
    # Check if AnkiConnect is up
    deck_names = get_deck_names_and_ids()
    if not deck_names:
        print("Error with Anki Connect, no new notes are added")
        return

    # Args parser for add notes from csv
    parser = argparse.ArgumentParser(description="A script that read a csv file and add automatically notes to Anki through Anki Connect.")
    parser.add_argument("--deck_name", help="The name of the Anki deck where to add notes")
    parser.add_argument("--f", "--file-name", help="The path to the file containing your notes")
    parser.add_argument("--find_note", help="Specify a textual clue to use to find a note")
    parser.add_argument("--get_note_by_id", help="Specify an id and return note front and back")
    parser.add_argument("--update_note_by_id", help="Edit a note by id")
    parser.add_argument("--new_front_text")
    parser.add_argument("--new_back_text")

    # Args parser for editing notes
    args = parser.parse_args()

    if args.find_note:
        card_ids = get_cards_id_by_query("A problem-solving agent is one that considers")
        if len(card_ids) != 0:
            card_id = card_ids[0]
            print(card_id)
    if args.get_note_by_id:
        ids = list()
        ids.append(int(args.get_note_by_id))
        note_info = get_notes_info_by_id(ids)

        note_fields = note_info[0]['fields']
        for field in note_fields:
            print(f"{field} : {note_fields[field]['value']}")

        #print(note_info["fields"])
    if args.update_note_by_id:
        ids = list()
        ids.append(int(args.update_note_by_id))
        note_info = get_notes_info_by_id(ids)

        result = update_note(ids[0], front=args.new_front_text, back=args.new_back_text)

    elif args.f and args.deck_name:
        add_notes_from_csv_file(args.f, args.deck_name)
        print("Script correctly finished!")

    return 0

if __name__ == "__main__":
    main()
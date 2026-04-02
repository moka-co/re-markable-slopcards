from src.notes import add_note, get_cards_id_by_query, get_note_by_id, update_note_by_id, add_notes_from_csv_file
from src.decks import get_deck_names_and_ids
import requests
import re
import csv
import argparse


# Logger
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
 

# Main function
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
        card_ids = get_cards_id_by_query(args.find_note)
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
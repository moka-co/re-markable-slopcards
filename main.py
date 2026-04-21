import src.notes as notes
import src.utils.check_anki as check_anki
import argparse
import logging

# Logger
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)


# Main function
def main() -> int:
    # Args parser for add notes from csv
    parser = argparse.ArgumentParser(
        description="A script that read a csv file and add automatically notes to Anki through Anki Connect."
    )
    parser.add_argument(
        "--deck_name", help="The name of the Anki deck where to add notes"
    )
    parser.add_argument(
        "--f", "--file-name", help="The path to the file containing your notes"
    )
    parser.add_argument(
        "--find_note", help="Specify a textual clue to use to find a note"
    )
    parser.add_argument(
        "--get_note_by_id", help="Specify an id and return note front and back"
    )
    parser.add_argument("--update_note_by_id", help="Edit a note by id")
    parser.add_argument("--new_front_text")
    parser.add_argument("--new_back_text")
    parser.add_argument(
        "--check_anki", action="store_true", help="Check if Anki is running and exit"
    )
    parser.add_argument(
        "--try_launch_anki",
        action="store_true",
        help="Calls a script that make a tentative to launch Anki",
    )

    # Args parser for editing notes
    args = parser.parse_args()

    if args.find_note:
        card_ids = notes.get_cards_id_by_query(args.find_note)
        if card_ids is not None and len(card_ids) != 0:
            card_id = card_ids[0]
            print(card_id)
    elif args.get_note_by_id:
        ids = list()
        ids.append(int(args.get_note_by_id))
        note_info = notes.get_notes_info_by_id(ids)

        if note_info is not None:
            note_fields = note_info[0]["fields"]
            for field in note_fields:
                print(f"{field} : {note_fields[field]['value']}")
    elif args.update_note_by_id:
        ids = list()
        ids.append(int(args.update_note_by_id))
        note_info = notes.get_notes_info_by_id(ids)

        notes.update_note(ids[0], front=args.new_front_text, back=args.new_back_text)
    elif args.f and args.deck_name:
        notes.add_notes_from_csv_file(args.f, args.deck_name)
    elif args.check_anki:
        # Check if Anki is Running
        if check_anki.is_anki_running():
            logger.info("Anki is running")
        else:
            logger.error(
                "Anki is not running. Please start it before calling any other functions. You can try `--try_launch_anki` or starting it manually"
            )

        # Check if AnkiConnect works
        if check_anki.is_endpoint_active():
            logger.info("Anki Connect add-on is up and working")
        else:
            logger.error("Anki Connect is not reachable")
    elif args.try_launch_anki:
        check_anki.try_launch_anki()

    return 0


if __name__ == "__main__":
    main()

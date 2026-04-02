---
name: note-to-anki-flashcards-manager
description: manager that help to add notes and generate
---

# Instructions

**Add notes from a CSV file**
Run `main.py` with the following arguments:
1. `--f file_name.csv` that is the file name, the file name must be a `.csv` file
2. `--deck_name "deck name"` that is provided by the user. If the user didn't provide one, ask him for the deck name

**Edit a note**:
First **search the note id** by running `main.py` with the following argument:
-  `--find_note your_clue` substitute "your_clue" with a clue, typically provided by the user

This will return three useful informations:
- The **note id**
- The front text
- The back text

Now edit the note specifying the note id, run `main.py` with the following arguments:
- `--update_note_by_id card_id` 
- (OPTIONAL) `--new_front_text "Updated fresh new front text"`
- (OPTIONAL) `--new_back_text "Better back text"`

Use the correct option depending on what you need to do e.g. an user may ask you to add more context in a cloze note; in such case you need to first generate the new back text by improving the previous one, then run the script `main.py --update_note_by_id insert_card_id_here --new_back_text "insert_new_back_text_here"` by utilizing the proper values for the arguments.


Ensure that the script runned correctly by checking the output. Notice the user of any results.

If you are on Windows try using `python3` instead of `python`.
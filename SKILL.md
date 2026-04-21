---
name: slopcards-to-anki
description: Manages Anki flashcards via AnkiConnect - adds flashcards from CSV files, searches existing flashcards, and updates card content. Use when working with Anki flashcards, CSV imports, spaced repetition, or when user mentions Anki, flashcards, or flashcard management.
---

#  Slopcard2Anki - Anki Flashcard Manager
This skill allows Claude/Gemini to read local files, distill them into high-quality flashcards, and sync them to Anki via a local `main.py` script.

## Core Workflow
When a user asks to "make flashcards" from a file or text, follow these steps:
1. **Analyze:** Read the source file/text provided by the user.
2. **Extract:** Identify key concepts suitable for Spaced Repetition.
3. **Generate CSV:** Create a temporary file (e.g., `tmp_cards.csv`) using the format defined below.
4. **Execute:** Run `python3 main.py --f tmp_cards.csv --deck_name "Target Deck"`.
5. **Clean up:** Delete the temporary CSV file after a successful run.

## Card Creation Principles 
To ensure high-quality cards, follow these rules when generating content:
- **Atomicity:** One card = one specific fact. Do not cram whole paragraphs into the 'back'.
- **Clarity:** Use bold text for key terms.
- Follow Data sanization rules
- **Cloze Deletion**: some cards and concepts must be cloze e.g. Front: "The derivative of an exponential is \_\_\_\_" Back: "Another derivative". You can use Anki's Cloze format: "{{c1::hidden text}}". 
    - *Example Front:* "The derivative of an exponential is {{c1::another derivative}}."
- **Formula Integrity:** If a formula is present, preserve it exactly using LaTeX syntax.
    - Use $formula$ for inline math.
    - USE $$formula$$ for display style math
- **The "Principle of Two-Way" (Optional):** For key formulas, create two cards: 
   - Card A: Name/Concept -> Formula
   - Card B: Formula -> Name/Concept/Variable definitions.
- **Context through wikilinks**: if a markdown file has wikilink, generate atleast 1 question that recall that wikilinked argument (reading the wikilinked reference!), make sure the note make sense in the context of the note
- **Output:** Write the flashcards into a temporary .csv file.

### Data Sanization
- Ensure LaTeX backslashes (\\) are preserved and not treated as escape characters by the CLI.
- Replace internal newlines with <br>
- Escape double quotes by doubling them ("").

## Constraints
When you are creating less than 100 cards, do not create Python script when creating the CSV file. Directly output the raw CSV data to the file.

### CSV Format Required
The `main.py` script expects a standard CSV with a header row. Use this structure:
```csv
front, back
"What is the capital of France?", "Paris"
```


## Add flashcards from a CSV file
Import flashcards from a CSV file:
`main.py --f file_name.csv --deck_name "Deck Name"`

**CSV format required**:
- `front`: The question or prompt
- `back`: The answer or explanation

If the user doesn't specify a deck name, ask them which deck to use. Never assume the deck name.

## Searching for flashards
Find a flashcard by keyword:
`main.py --find_note "search term"`

Returns:
- CARD ID (needed for updates)
- Front text
- Back text

If multiple flashcards match, review the returned text to identify the correct flashcard.

## Updating cards

Update an existing flashcard using its ID::
- To update front: `main.py --update_note_by_id CARD_ID --new_front_text "Updated fresh new front text"`
- To update back: `main.py --update_note_by_id CARD_ID --new_back_text "Better back text"`
- To update both: include both `--new_front_text` and `--new_back_text` flags

To update both use:
```bash
main.py --update_note_by_id CARD_ID --new_front_text "New front" --new_back_text "New back"
```

**Workflow for enhancing an existing cards:**
1. Search for the flashcard: `main.py --find_note "keyword"`
2. Review existing back text
3. Generate improved back text with additional context, you may ask the user where to look for context
4. Update `main.py --update_note_by_id CARD_ID --new_back_text "Enhanced text with extra context"`

Ensure that the script runned correctly by checking the output. Notice the user of any output you see.

## Troubleshooting
Always notify the user of any error you encounter.

**If Anki is not running**
1. Run this exact command `main.py --anki_check`
2. Attempt auto-launch with this exact command: `main.py --try_launch_anki`
3. If auto-launch fails, notice the user and ask him to start Anki.

**If flashcard not found**
- Try broader search terms
- Check if card exists in the correct deck
- Ask the user for what to do

**On Windows:**
Use `python3 main.py` instead of `python main.py` if you encounter errors.
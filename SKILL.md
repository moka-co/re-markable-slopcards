---
name: slopcards-to-anki
description: Manages Anki flashcards via AnkiConnect - adds flashcards from CSV files, searches existing flashcards, and updates card content. Use when working with Anki flashcards, CSV imports, spaced repetition, or when user mentions Anki, flashcards, or flashcard management.
---

#  Slopcard2Anki - Anki Flashcard Manager
This skill allows Claude/Gemini to read local files, distill them into high-quality flashcards, and sync them to Anki via a local `skill/main.py` script.

## Operational Environment
This skill operates exclusively in a **local execution context**. It requires access to the host machine's filesystem to read/write CSV files and access to `localhost:8765` to communicate with AnkiConnect. If you are being executed in a cloud-hosted web sandbox (e.g., a browser-based chat interface), notify the user that you cannot reach their local Anki instance and recommend using a local CLI-based agent instead.

## Prerequisites
Ensure the environment has the necessary dependencies:
```shell
python -m pip install requests psutil
```

## Card Creation Principles
When generating content, adhere to these "Gold Standard" SR (Spaced Repetition) rules:
To ensure high-quality cards, follow these rules when generating content:
- **Atomicity:** One card = one specific fact. Avoid "wall-of-text" answers
- **Clarity:** **bold** key terms for visual scanning.
- Follow Data sanization rules
- **Cloze Deletion**: some cards and concepts must be cloze e.g. Front: "The derivative of an exponential is \_\_\_\_" Back: "Another derivative". You can use Anki's Cloze format: "{{c1::hidden text}}". 
    - *Example:* "{{c1::Rome}} is the capital of Italy."
- **Formula Integrity:** If a formula is present, preserve it exactly using LaTeX syntax.
    - Use $inline math$ for small variables.
    - Use $$display math$$ for standalone equations.
- **The "Principle of Two-Way" (Optional):** For key formulas, generate two cards: 
   - Card A: Name/Concept -> Formula
   - Card B: Formula -> Concept/Variable definitions.
- **Contextual Wikilinks**: If a markdown file contains [[wikilinks]], generate at least one question that references the linked concept (reading the linked file if available)
- **Output:** Write the flashcards into a temporary .csv file under `.tmp/` directory e.g. `./tmp/tmp_flashcards.csv`.

## Data Sanization
To ensure the CLI parses the data correctly, you **must**:
- **No Headers**: do **not** include "Front, Back" headers rows in the CSV
- **Escaping**: escape double quotes by doubling them ("").
- **Newlines**: replace internal newlines with <br>
- **LaTeX**: ensure LaTeX backslashes (\\) are preserved and not treated as escape characters by the CLI.

## CSV Format Required
The `main.py` script expects a standard CSV with a header row. Use this structure:
```csv
"What is the capital of France?", "Paris"
"{{c1::Rome}} is the capital of Italy", "and the most populated municipality of Italy"
```

- The first field is the `front` that is the question or the prompt
- The second field is the `back` that is the answer or explanation



## Core Workflows

### Workflow 1 - Generate flashcards and upload 
When a user provides a file or text and asks for "flashcards", follow these steps:
1. **Analyze:** Read the source file/text provided by the user.
2. **Extract:** extract concepts suitable for Spaced Repetition.
3. **Sanitize**: apply the [[Data Sanization]] rules above
3. **Generate CSV:** Create a temporary file (e.g., `tmp_cards.csv`) using the format defined below.
4. **Execute:** Run `python -m skill.main --f tmp_cards.csv --deck_name "Target Deck"`.
5. **Clean up:** Delete the temporary CSV file after a successful run.

**Constraint**: if generating <100 cards, **do not** write a Python script to build the CSV; directly output the raw CSV data to a file.

### Workflow 2 - Import
To import an **existing** CSV file:
```shell
python -m skill.main --f file_name.csv --deck_name "Deck Name"
```
*Note:* if no deck name is provided, prompt the user for one. Never assume the deck name.

## Workflow 3 - Search & Discovery
To find a flashcard by keyword:
```shell
python -m skill.main --find_note "search term"
```

Returns:
- CARD ID (needed for updates)
- Front text
- Back text

If multiple flashcards match, review the returned text to identify the correct flashcard.

### Workflow 4: Update Flashcards
1. **Search**: find the ID via `python -m skill.main --find_note` follow instruction from [[Workflow 3 - Search & Discovery]]
2. Review the return back text and improve it by adding additional context
    - You may ask the user for a file where to look for additional context
3. **Update**: 
```shell
python -m skill.main --update_note_by_id CARD_ID --new_front_text "New front" --new_back_text "New back"
```

*Note* you can also include only one of the back/front arguments e.g. to update only back: `python -m skill.main --update_note_by_id CARD_ID --new_back_text "Better back text"`

## Troubleshooting
Always notify the user of any error you encounter.

**If Anki is not reachable/running**
1. Attempt auto-launch with this command: `python -m skill.main --try_launch_anki`
2. If auto-launch fails, notice the user and ask him to start Anki.

**If flashcard not found**
- Try broader search terms
- Check if card exists in the correct deck
- Ask the user for what to do

**On Windows:**
If the standard `python -m skill.main` fails, ensure your environment is set up correctly for `src` to be in your PYTHONPATH, or run it from the project root.

---

**Important**: always report the CLI output to the user to confirm the action was successful
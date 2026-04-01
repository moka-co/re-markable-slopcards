import requests 
from dataclasses import dataclass, field
from typing import Optional
import json 
import re

ENDPOINT="http://127.0.0.1:8765" # AnkiConnect works only locally

@dataclass
class NoteBuilder:
    """
    Builder for AnkiConnect 'add_note' payloads.

    Usage:
        note = (
            NoteBuilder()
            .deck("My Deck")
            .model("Basic")
            .field("Front", "What is the capital of France?")
            .field("Back", "Paris")
            .tag("geography")
            .allow_duplicates(False)
            .build()
        )
    """

    _deck_name: str = ""
    _model_name: str = ""
    _fields: dict = field(default_factory=dict)
    _tags: list = field(default_factory=list)
    _allow_duplicates: bool = False


    def deck(self, deck_name: str) -> "NoteBuilder":
        self._deck_name = deck_name
        return self

    def model(self, model_name: str) -> "NoteBuilder":
        self._model_name = model_name
        return self


    def tag(self, *tags: str) -> "NoteBuilder": 
        self._tags.extend(tags)
        return self

    def allow_duplicates(self, allow: bool) -> "NoteBuilder":
        self._allow_duplicates = allow
        return self
    
    def add_field(self, name: str, value: str) -> "NoteBuilder":
        self._fields[name] = value
        return self
    
    def basic(self, front: str, back: str) -> "NoteBuilder":
        return self.model("Basic").add_field("Front",front).add_field("Back",back)
    
    def cloze(self, text: str, back_extra: str = "") -> "NoteBuilder":
        """Shorthand for a Cloze note. Text must contain {{c1::...}} markers."""
        return self.model("Cloze").add_field("Text", text).add_field("Back Extra", back_extra)

    def _validate(self):
        errors = []
        if not self._deck_name:
            errors.append("Deck name is required.")
        if not self._model_name:
            errors.append("Model name is required.")
        if not self._fields:
            errors.append("At least one field is required.")
        if self._model_name == "Cloze" and "Text" in self._fields:
            if "{{c" not in self._fields["Text"]:
                errors.append("Cloze note 'Text' field must contain at least one {{c1::...}} marker.")
        if errors:
            raise ValueError("NoteBuilder validation failed:\n" + "\n".join(f"  - {e}" for e in errors))


    def build(self) -> dict:
        """Returns the raw AnkiConnect payload dict."""
        self._validate()
        return {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": self._deck_name,
                    "modelName": self._model_name,
                    "fields": self._fields,
                    "tags": self._tags,
                    "options": {
                        "allowDuplicate": self._allow_duplicates,
                    },
                }
            },
        }


# These notes comes from obsidian where bold formatting is done with "**" around words"
# However, Anki wants a different format i.e. <b>word</b>
# A similar issue with Latex
def fix_formatting(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    result = re.sub(r'\$(.*?)\$', r'\(\1\)', text)
    return result

# Add a note to an Anki Deck 
# You need to specify: a deck name (that must exists), a model name (that must be allowed), a front content and back content
def add_note(deck_name, model_name, front_content, back_content):
    #print(f"Deck Name: {deck_name}\n Model Name: {model_name}\n Front Content: {front_content}\n Back Content: {back_content}")

    front_content = fix_formatting(front_content)
    back_content = fix_formatting(back_content)

    payload_builder = NoteBuilder().deck(deck_name)
    if model_name == "Cloze":
        payload_builder= payload_builder.cloze(front_content,back_content)
    else:
        payload_builder = payload_builder.basic(front_content,back_content)

    payload = payload_builder.build()

    response = requests.post(ENDPOINT, json=payload) # Make request
    if not response.status_code == 200: #OK
        print("Error, printing full body response\n")
        body=response.json()
        print(body)
    
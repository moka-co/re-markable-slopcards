# Slopcards to Anki
`slopcards-to-anki` is a local AI skill that empowers Claude/Gemini to transform markdown notes into high-retention flashcards. It automatically uploads and syncs them to your local Anki profile. Works great with PKMs like obsidian.md.

## Features
- **Automatic Upload & Sync**: from your favorite AI CLI tool
- **LaTeX Support**: Perfect for STEM students, automatically handles math blocks for Anki's rendering engine. 
- **Smart Context**: Claude/Gemini can see your files and directory, so they can generate better flashcards by understanding the context of your notes

## Quick Start

### Prerequisites
- [Anki](https://apps.ankiweb.net/) must be installed and running
- [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on installed (Code: `2055492159`), leave default configuration

### Installation
Follow your favorite tool instructions on how to add this skill. 
Usually it involve cloning this repo into a `.skills` directory:
```bash
git clone https://github.com/moka-co/slopcards2anki.git
```

### Usage
Once the skill is added to Claude Code / Gemini CLI / Qwen CLI, you can type a prompt like this:
```text
Convert "My/Study/Note.md" into 30 atomic Anki flashcards using slopcards-to-anki SKILL
```

## Limitations
This skill currently doesn't support images upload to notes. **As far as i know** and **with the tools i have tested** (Gemini and Qwen) they don't make flashcards with images. Very rarely i have seen Gemini making flashcards with "textual description" of a very simple image like a diagram.

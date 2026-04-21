# Slopcards to Anki
`slopcards-to-anki` is a local AI skill that empowers Claude/Gemini to transform markdown notes into high-retention flashcards. It automatically uploads and syncs them to your local Anki profile. Works great with PKMs like obsidian.md.

## Features
- **Automatic Upload & Sync**: from your favorite AI CLI tool
- **LaTeX Support**: Perfect for STEM students, automatically handles math blocks for Anki's rendering engine. 
- **Smart Context**: Claude/Gemini can see your files and directory, so they can generate better flashcards by understanding the context of your notes

## Quick Start

1. Prerequisites
- Anki must be installed and running
- AnkiConnect add-on installed (Code: 2055492159), leave default configuration

2. Installation
Follow your favorite tool instructions on how to add this skill. 
Usually it involve cloning this repo into a `.skills` directory:
```bash
git clone https://github.com/moka-co/slopcards2anki.git
```

3. Usage
Once the skill is added to Claude Code / Gemini CLI / Qwen CLI, you can type a prompt like this:
```text
Read @My/Study/Note.md, make 30 high-retention flashcards and use slopcards-to-anki skill to upload them to anki
```
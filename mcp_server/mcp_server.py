from fastmcp import FastMCP
from src import decks, notes
from src.utils import check_anki
from pathlib import Path
import logging


# Initialize FastMCP server
mcp = FastMCP(
    "slopcards2anki", instructions=Path("./mcp_server/INSTRUCTIONS.MD").read_text()
)

# Configure logging to not interfere with stdio transport
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="./mcp_debug.log",
    filemode="a",
)
logger = logging.getLogger(__name__)

# Ensure the file is writable
logger.info("MCP Server started and logging initialized.")


@mcp.tool()
def list_anki_decks() -> list[str]:
    """List all available Anki decks."""
    deck_data = decks.get_deck_names_and_ids()
    if deck_data:
        return list(deck_data)
    return []


@mcp.tool()
def create_anki_deck(name: str) -> str:
    """Create a new Anki deck with the given name."""
    result = decks.create_deck(name)
    if result:
        return result
    return "Error when creating deck name"


@mcp.tool()
def add_cards_from_csv(file_path: str, deck_name: str) -> str:
    """Add cards from a CSV file to a specific Anki deck."""
    try:
        notes.add_notes_from_csv_file(file_path, deck_name)
        return f"Processed cards from {file_path} for deck '{deck_name}'."
    except Exception as e:
        return f"Error processing CSV: {str(e)}"


@mcp.tool()
def find_cards_by_text(query: str) -> list[int]:
    """Find Anki note IDs matching a textual query."""
    result = notes.get_cards_id_by_query(query)
    if result:
        return result
    return []


@mcp.tool()
def update_anki_note(note_id: int, front: str = "", back: str = "") -> str:
    """Update the front (Text) or back (Back Extra) of an existing note by ID."""
    result = notes.update_note(note_id, front=front, back=back)
    if result:
        return f"Note {note_id} updated successfully."
    return f"Failed to update note {note_id}."


@mcp.tool()
def launch_anki() -> str:
    """Attempt to launch Anki if it is not running."""
    check_anki.try_launch_anki()
    return "Attempted to launch Anki. Please wait a few seconds for it to start."


@mcp.tool()
def get_anki_status() -> str:
    """Check if Anki and AnkiConnect are running."""
    running = check_anki.is_anki_running()
    connected = check_anki.is_endpoint_active()
    return f"Anki Running: {running}\nAnkiConnect Active: {connected}"


# Read INSTRUCTIONS.MD for troubleshooting
@mcp.resource(uri="file://INSTRUCTIONS.MD")
def get_guidance() -> str:
    path = Path("./mcp_server/INSTRUCTIONS.MD")
    if not path.exists():
        raise FileNotFoundError("File INSTRUCTIONS.MD not found")
    return path.read_text()


if __name__ == "__main__":
    try:
        logger.error("Before MCP RUN")
        mcp.run()
    except Exception as e:
        logger.exception(f"The server encountered a fatal error during startup: {e}")
        raise

from fastmcp import FastMCP
from src import decks, notes
from src.utils import check_anki
from pathlib import Path
import logging
import sys 

# Initialize FastMCP server
mcp = FastMCP("slopcards2anki")

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


"""
# Expose SKILL.MD
@mcp.resource(uri="file://SKILL.MD")
def get_skill() -> str:
    path = Path(f"./SKILL.MD")
    if not path.exists():
        raise FileNotFoundError(f"File SKILL.MD not found")
    return path.read_text()
"""


if __name__ == "__main__":
    try:
        mcp.run()
    except Exception as e:
        logger.exception(f"The server encountered a fatal error during startup: {e}")
        raise

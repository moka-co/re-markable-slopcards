@echo off 
cd /d "%~dp0"
cd ..
python3 -m uv run --project C:\\Users\\tech\\Documents\\GitHub\\slopcards2anki python -m mcp_server.mcp_server
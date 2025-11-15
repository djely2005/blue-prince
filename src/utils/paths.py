# src/utils/paths.py
from pathlib import Path

# This file is located in src/utils → so "parents[1]" brings us back to src/
SRC_DIR = Path(__file__).resolve().parents[1]

# Path to src/assets/
ASSETS_DIR = SRC_DIR / "assets"

def asset_path(relative: str) -> str:
    """
    Returns the absolute path to an asset located inside src/assets/.
    Example: asset_path("rooms/red_room.png")
    """
    return (ASSETS_DIR / relative).as_posix()

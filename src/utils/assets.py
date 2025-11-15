# src/utils/assets.py
import pygame
from typing import Dict
from src.utils.paths import asset_path

# Cache: avoids reloading the same image multiple times
_surface_cache: Dict[str, pygame.Surface] = {}

def load_image(relative_path: str) -> pygame.Surface:
    """
    Loads an image from src/assets/<relative_path>.
    Uses a cache so repeated calls are instant.
    Example: load_image("rooms/red_room.png")
    """
    # Already loaded? Return it
    if relative_path in _surface_cache:
        return _surface_cache[relative_path]

    # Not loaded yet → load it from disk
    full_path = asset_path(relative_path)
    image = pygame.image.load(full_path).convert_alpha()

    # Store in cache
    _surface_cache[relative_path] = image
    return image


# main.py

import pygame
import sys
from src.settings import MAP_WIDTH, INFO_WIDTH, GRAY, DARK_BLUE, BLUE, WIDTH, HEIGHT, TILE_SIZE, OFFSET_X
from src.entities.map import game_map
from src.session import session
from src.entities.choice_menu import menu
from src.entities.door import Door
from src.ui.hud import HUD
from src.ui.room_selector import RoomSelector


# Change to put Map class
def draw_map_area(screen):
    """Draw the left-side map area."""
    map_rect = pygame.Rect(0, 0, MAP_WIDTH, HEIGHT)
    pygame.draw.rect(screen, BLUE, map_rect)


def main():
    pygame.init()
    pygame.display.set_caption("Blue Prince - Prototype Display")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    FONT = pygame.font.Font(None, 28)
    
    # Create HUD for displaying inventory
    hud = HUD(rect=(MAP_WIDTH, 0, INFO_WIDTH, HEIGHT), font=FONT)
    
    # Create room selector for when doors are opened
    room_selector = RoomSelector(rect=(MAP_WIDTH, 0, INFO_WIDTH, HEIGHT), font=FONT)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle room selector first if active
            if room_selector.active:
                result = room_selector.handle_event(event)
                if isinstance(result, str) and result == "reroll":
                    # Handle reroll request
                    if session.player.inventory.dice.quantity >= room_selector.reroll_cost:
                        # Deduct dice and get new room choices
                        session.player.inventory.spend_dice(room_selector.reroll_cost)
                        # Double the cost for next reroll
                        room_selector.reroll_cost *= 2
                        # Re-request room placement with new weighted choices
                        # We need to store the current door position/direction from the last open_door_callback
                        # For now, we'll use the player's selected direction and position
                elif result and result != "reroll":
                    # Room was selected
                    game_map.handle_room_selection(result, session.player)
                continue

            # MENU INPUT HANDLING
            menu.handle_event(event, session.player)

        # --- Draw everything ---
        screen.fill(DARK_BLUE)
        game_map.draw(screen)
        game_map.update_selected_direction(session.player, screen)
        game_map.draw_player_position(screen, session.player)
        
        # Draw HUD or room selector
        if room_selector.active:
            room_selector.draw(screen)
        else:
            hud.draw(screen, session.player)

        menu.choices = []
        if session.player.selected and not room_selector.active:
            doors = [e for e in game_map.grid[session.player.grid_position[0]][session.player.grid_position[1]].doors if e.direction == session.player.selected]
            if doors:
                door = doors[0]
                # Create callback that opens door and shows room selector
                def open_door_callback(player, d=door, pos=session.player.grid_position, direction=session.player.selected):
                    if d.open_door(player):
                        # Door opened successfully, show room selector
                        room_choices = game_map.request_place_room(pos, direction, player)
                        room_selector.set_choices(room_choices)
                    else:
                        # Not enough keys
                        pass
                
                menu.choices.append(
                    (f"Open Door - Cost {door.lock_state.value} keys", open_door_callback)
                )
        
        # Add options to move to adjacent visited rooms
        adjacent_visited = game_map.get_adjacent_visited_rooms(session.player.grid_position)
        for direction, room in adjacent_visited.items():
            direction_name = direction.name.capitalize()
            menu.choices.append(
                (f"Go {direction_name} ({room.name})", lambda player, d=direction: game_map.move_to_adjacent_room(player, d))
            )

        # Draw the right menu (always draw unless in room selector mode)
        if not room_selector.active:
            menu.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()

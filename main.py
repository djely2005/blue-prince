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
from src.entities.yellow_room import Commissary, LaundryRoom, YellowRoom


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
        # Prepare menu choices each frame (shops take priority)
        menu.choices = []
        shop_active = False
        current_room = game_map.grid[session.player.grid_position[0]][session.player.grid_position[1]]
        if isinstance(current_room, YellowRoom) and getattr(current_room, 'possible_item', None):
            shop_items = current_room.possible_item
            for shop_item in shop_items:
                if isinstance(shop_item.item, dict):
                    desc = shop_item.item.get('desc', shop_item.item.get('service', 'Service'))
                    label = f"{desc} - Cost: {shop_item.price}"
                else:
                    owned = ' (Owned)' if getattr(shop_item, 'owned', False) else ''
                    label = f"Buy {getattr(shop_item.item, 'name', str(shop_item.item))} - Cost: {shop_item.price}{owned}"

                def make_buy_callback(si, room):
                    def cb(player):
                        inv = player.inventory
                        if si.price > inv.money.quantity:
                            return
                        inv.spend_money(si.price)
                        if isinstance(room, LaundryRoom) and isinstance(si.item, dict):
                            room.perform_service(player, si.item.get('service'))
                            return
                        itm = si.item
                        if hasattr(itm, 'type'):
                            if itm.type.name == 'MONEY':
                                inv.add_money(itm.quantity)
                            elif itm.type.name == 'GEM':
                                inv.add_gems(itm.quantity)
                            elif itm.type.name == 'KEY':
                                inv.add_keys(itm.quantity)
                            elif itm.type.name == 'STEP':
                                inv.add_steps(itm.quantity)
                            elif itm.type.name == 'DICE':
                                inv.add_dice(itm.quantity)
                        else:
                            inv.permanentItems.append(itm)
                            si.mark_owned(True)

                    return cb

                menu.choices.append((label, make_buy_callback(shop_item, current_room)))
            shop_active = True

        # If not in a shop, populate door and movement choices now so they are available during event handling
        if session.player.selected and not room_selector.active:
            doors = [e for e in game_map.grid[session.player.grid_position[0]][session.player.grid_position[1]].doors if e.direction == session.player.selected]
            if doors:
                door = doors[0]
                def open_door_callback(player, d=door, pos=session.player.grid_position, direction=session.player.selected):
                    if d.open_door(player):
                        room_choices = game_map.request_place_room(pos, direction, player)
                        room_selector.set_choices(room_choices)
                menu.choices.append((f"Open Door - Cost {door.lock_state.value} keys", open_door_callback))

        # Add options to move to adjacent visited rooms
        adjacent_visited = game_map.get_adjacent_visited_rooms(session.player.grid_position)
        for direction, room in adjacent_visited.items():
            direction_name = direction.name.capitalize()
            menu.choices.append((f"Go {direction_name} ({room.name})", lambda player, d=direction: game_map.move_to_adjacent_room(player, d)))

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
        game_map.draw(screen, session.player)
        game_map.update_selected_direction(session.player, screen)
                
        # Draw HUD or room selector (pass current room into selector)
        current_room = game_map.grid[session.player.grid_position[0]][session.player.grid_position[1]]
        if room_selector.active:
            room_selector.draw(screen, current_room)
        else:
            hud.draw(screen, session.player)

        
        

        # Draw the right menu (always draw unless in room selector mode)
        if not room_selector.active:
            menu.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()

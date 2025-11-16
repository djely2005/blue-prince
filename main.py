# main.py

import pygame
import sys
import random
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
    # Ask for a seed before initializing pygame so the user can enter one or get a random seed
    seed_input = input("Enter seed (leave empty for random): ").strip()
    if seed_input == "":
        seed = random.randint(0, 2**31 - 1)
    else:
        try:
            seed = int(seed_input)
        except Exception:
            # allow non-numeric seeds by hashing
            seed = abs(hash(seed_input)) % (2**31)

    print(f"Using seed: {seed}")

    pygame.init()
    pygame.display.set_caption("Blue Prince - Prototype Display")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    FONT = pygame.font.Font(None, 28)
    
    # Create HUD for displaying inventory
    hud = HUD(rect=(MAP_WIDTH, 0, INFO_WIDTH, HEIGHT), font=FONT)
    
    # Create room selector for when doors are opened
    room_selector = RoomSelector(rect=(MAP_WIDTH, 0, INFO_WIDTH, HEIGHT), font=FONT)

    # Initialize/reset the global map with the chosen seed
    try:
        game_map.reset(seed)
        game_map.seed = seed
    except Exception:
        # If reset is not available for some reason, ignore (map was initialized at import)
        pass
    # Ensure session and global random use the same seed for deterministic behavior
    try:
        from src import session as session_module
        session_module.session.seed = seed
        session_module.session.random = random.Random(seed)
    except Exception:
        # fallback: if session can't be updated, seed the global random module
        pass
    # Also seed the global random module so modules using module-level `random` are deterministic
    random.seed(seed)

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
                            player.add_permanent_item(itm)
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
                
                if (not(game_map.check_if_room_exist_in_position(session.player, door.direction))): menu.choices.append((f"Open Door - Cost {door.lock_state.value} keys", open_door_callback))

        # If current room has an event, show an interact option
        if not room_selector.active:
            current_room = game_map.grid[session.player.grid_position[0]][session.player.grid_position[1]]
            evt = getattr(current_room, 'event', None)
            if evt is not None and not getattr(evt, 'opened', False):
                # Add menu choice to interact/open the event
                def make_event_cb(e):
                    def cb(player):
                        try:
                            res = e.open(player)
                        except Exception as exc:
                            hud.show_message(f"Error: {exc}", 3.0)
                            return
                        # Expect (success: bool, message: str, reward: dict)
                        if isinstance(res, tuple) and len(res) >= 2:
                            success, msg = res[0], res[1]
                        else:
                            success, msg = False, 'Nothing happened'
                        hud.show_message(msg, 3.0)

                    return cb

                menu.choices.append((f"Interact: {evt.name}", make_event_cb(evt)))

        # Add options to move to adjacent visited rooms
        adjacent_visited = game_map.get_adjacent_visited_rooms(session.player.grid_position)
        for direction, room in adjacent_visited.items():
            direction_name = direction.name.capitalize()
            menu.choices.append((f"Go {direction_name} ({room.name})", lambda player, d=direction: game_map.move_to_adjacent_room(player, d)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle HUD click for consuming OtherItems
            if event.type == pygame.MOUSEBUTTONDOWN and not room_selector.active:
                clicked_item = hud.handle_click(event.pos)
                if clicked_item is not None:
                    msg = session.player.inventory.use_other_item(clicked_item)
                    hud.show_message(msg, 3.0)
                    continue

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
        # Draw seed on the HUD area
        try:
            seed_surf = FONT.render(f"Seed: {seed}", True, (0, 0, 0))
            screen.blit(seed_surf, (MAP_WIDTH + 10, 8))
        except Exception:
            pass
        
        # Draw HUD or room selector (pass current room into selector)
        current_room = game_map.grid[session.player.grid_position[0]][session.player.grid_position[1]]
        if room_selector.active:
            room_selector.draw(screen, current_room)
        else:
            hud.draw(screen, session.player)

        
        

        # Draw the right menu (always draw unless in room selector mode)
        if not room_selector.active:
            menu.draw(screen)

        # Check for losing condition: steps reached zero
        if session.player.inventory.steps.quantity <= 0 and not getattr(game_map, 'game_over', False):
            game_map.game_over = True
            game_map.game_over_message = "You ran out of steps!"
            game_map.game_over_reason = 'lose'

        # If the map signalled game over, show overlay and exit
        if getattr(game_map, 'game_over', False):
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            big_font = pygame.font.Font(None, 64)
            
            # Display different messages for win/loss
            reason = getattr(game_map, 'game_over_reason', 'win')
            if reason == 'win':
                title = big_font.render("You Win!", True, (255, 215, 0))
                title_color = (255, 215, 0)
            else:
                title = big_font.render("Game Over!", True, (255, 0, 0))
                title_color = (255, 0, 0)
            
            title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 24))
            screen.blit(title, title_rect)
            msg_text = getattr(game_map, 'game_over_message', '') + f"  (Seed: {seed})"
            msg = FONT.render(msg_text, True, (255, 255, 255))
            msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 24))
            screen.blit(msg, msg_rect)
            pygame.display.flip()
            pygame.time.wait(4000)
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()

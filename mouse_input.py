from enum import Enum
from game import CATEGORIES
import text_utility as TEXT
""""""


""" Handle Mouse Clicks"""


""""""

def handle_mouse_press(game, x, y, _button, _modifiers, game_state):
    
    if game.stage == game_state.OUTSIDE:
        mouse_press_outside(game, x,y, game_state)
    elif game.stage == game_state.INTRO:
        mouse_press_intro(game,x,y,game_state)
    elif game.stage == game_state.SPREAD:
        mouse_press_spread(game,x,y,game_state)
    elif game.stage == game_state.READING_INTRO:
        mouse_press_reading_intro(game,x,y,game_state)
    elif game.stage in {
        game_state.READING_CARD_1,
        game_state.READING_CARD_2,
        game_state.READING_CARD_3,
    }:
        mouse_press_reading_cards(game,x,y,game_state)
    elif game.stage == game_state.READING_SUMMARY:
        mouse_press_reading_summary(game,x,y,game_state)

    if game.stage != game_state.TITLE:
         mouse_press_option_button(game, x,y, game_state)
    
    if game.menu_open:
         mouse_press_options_menu(game, x,y)


def mouse_press_outside(game, x, y, game_state):
    # print(f"Mouse clicked at ({x}, {y})")
    # print(f"game_state is {game.stage}")
    if game.x_right_button + 200 - game.button_clickbox_width // 2 <= x <= game.x_right_button + 200 + game.button_clickbox_width // 2 and \
            game.y_bottom_button <= y <= game.y_bottom_button - 50 + game.button_clickbox_height:
        
        game.sound_manager.play_sfx("button", volume=1.0)
        game.close()
        return
    if game.x_middle_button - game.button_clickbox_width <= x <= game.x_middle_button + game.button_clickbox_width and \
            game.y_bottom_button <= y <= game.y_bottom_button + game.button_clickbox_height:
        game.sound_manager.play_sfx("door", volume=1.0)
        game.stage = game_state.INTRO

def mouse_press_intro(game, x, y, _game_state):
            button_positions = [
                (275, 300),  # Button 0
                (650, 300),  # Button 1
                (1025, 300),  # Button 2
                (275, 150),  # Button 3
                (650, 150),  # Button 4
                (1025, 150)  # Button 5
            ]

            # Check if a button is clicked
            for i, (bx, by) in enumerate(button_positions):
                if bx - game.button_clickbox_width <= x <= bx + game.button_clickbox_width and by - (game.button_clickbox_height // 2) <= y <= by + game.button_clickbox_height:  # Button bounds
                    game.clicked_button = f"button_{i}"
                    game.sound_manager.play_sfx("button", volume=1.0)
                    game.set_intention(CATEGORIES[i])  # Set intention based on button index
                    return
                

def mouse_press_spread(game, x, y, _game_state):
            if game.reveal_active:
                if game.x_middle_button - game.button_clickbox_width <= x <= game.x_middle_button + game.button_clickbox_width and game.y_bottom_button  <= y <= game.y_bottom_button  + game.button_clickbox_height:
                    game.sound_manager.play_sfx("button", volume=1.0)
                    # Dismiss popup and place the revealed card in the corner
                    game.reveal_active = False

                    game.current_revealed_card = None
                    if len(game.selected_cards) == 2:
                        game.start_reading_button_active = True
                        print(f"is start reading active: {game.start_reading_button_active}")
                    if len(game.selected_cards) == 3:
                        game.drawn_cards = game.selected_cards
                        game.start_loading()
                        game.start_reading_button_active = False
                        print(f"is start reading active: {game.start_reading_button_active}")
                    return
                    
        
            if not game.reveal_active:
                for card in reversed(game.deck.cards):
                    if card.is_clicked(x, y):
                        game.deck.cards.remove(card)
                        game.sound_manager.play_sfx("card_move", volume=1.0)
                        game.reveal_card(card) 
                        # Trigger popup for selected card
                        return    

def mouse_press_reading_intro(game,x,y,game_state):
            
            if game.x_middle_button-game.button_clickbox_width <= x <= game.x_middle_button + game.button_clickbox_width and game.y_bottom_button <= y <= game.y_bottom_button + game.button_clickbox_height:
                advance_reading_stage(game, game_state)
                return
            

        
def mouse_press_reading_cards(game,x,y,game_state):
                
    if game.x_right_button-game.button_clickbox_width <= x <= game.x_right_button + game.button_clickbox_width and game.y_bottom_button  <= y <= game.y_bottom_button + game.button_clickbox_height:
        advance_reading_stage(game,game_state)
        return
    if game.x_left_button - game.button_clickbox_width <= x <= game.x_left_button + game.button_clickbox_width and game.y_bottom_button <= y <= game.y_bottom_button +game.button_clickbox_height:
        previous_reading_stage(game,game_state)
        return

def mouse_press_reading_summary(game,x,y, game_state):
    
    
    
    if game.x_middle_button - game.button_clickbox_width <= x <= game.x_middle_button + game.button_clickbox_width and game.y_bottom_button  <= y <= game.y_bottom_button +game.button_clickbox_height:
        game.reset_data()
        TEXT.reset_typing_state(game) 
        game.sound_manager.play_sfx("button", volume=1.0)
        game.stage = game_state.INTRO
    if game.x_left_button - 100 - game.button_clickbox_width <= x <= game.x_left_button- 100 + game.button_clickbox_width and \
        game.y_bottom_button <= y <= game.y_bottom_button + game.button_clickbox_height:
        previous_reading_stage(game, game_state)
        return
    if game.x_right_button+100 - game.button_clickbox_width <= x <= game.x_right_button+100 + game.button_clickbox_width and \
        game.y_bottom_button <= y <= game.y_bottom_button + game.button_clickbox_height:
        game.reset_data()
        TEXT.reset_typing_state(game) 
        game.sound_manager.play_sfx("door", volume=1.0)
        game.stage = game_state.OUTSIDE


def advance_reading_stage(game, game_state):
        """ Advance to the next reading stage. """
        if game.stage == game_state.READING_INTRO:
            game.stage = game_state.READING_CARD_1
            TEXT.reset_typing_state(game)  
            game.sound_manager.play_sfx("card_move", volume=1.0)
        elif game.stage == game_state.READING_CARD_1:
            game.stage = game_state.READING_CARD_2
            TEXT.reset_typing_state(game)
            game.sound_manager.play_sfx("card_move", volume=1.0)
        elif game.stage == game_state.READING_CARD_2:
            game.stage = game_state.READING_CARD_3
            game.sound_manager.play_sfx("card_move", volume=1.0)
            TEXT.reset_typing_state(game)  
        elif game.stage == game_state.READING_CARD_3:
            game.stage = game_state.READING_SUMMARY
            game.sound_manager.play_sfx("card_spread", volume=1.0)
            TEXT.reset_typing_state(game)  
        elif game.stage == game_state.READING_SUMMARY:
            print("Reading complete.")  # Placeholder for post-reading action

def previous_reading_stage(game, game_state):
    """Return to previous reading stage"""
    if game.stage == game_state.READING_CARD_1:
        game.stage = game_state.READING_INTRO
        TEXT.reset_typing_state(game) 
        game.sound_manager.play_sfx("button", volume=1.0)
    elif game.stage == game_state.READING_CARD_2:
        game.stage = game_state.READING_CARD_1
        TEXT.reset_typing_state(game) 
        game.sound_manager.play_sfx("card_move", volume=1.0)
    elif game.stage == game_state.READING_CARD_3:
        game.stage = game_state.READING_CARD_2
        game.sound_manager.play_sfx("card_move", volume=1.0)
        TEXT.reset_typing_state(game) 
    elif game.stage == game_state.READING_SUMMARY:
        game.stage = game_state.READING_CARD_3
        game.sound_manager.play_sfx("card_move", volume=1.0)
        TEXT.reset_typing_state(game) 

def mouse_press_option_button(game, x, y, game_state):
     if game.x_right_button + 250 - 100 <= x <= game.x_right_button + 250 + 100 and \
            900 -20 <= y <= 900 - 50 + 100:
        game.menu_open = True
        game.sound_manager.play_sfx("button", volume=1.0)

def mouse_press_options_menu(game, x, y):
      if game.menu_open:
        if 400 <= x <= 600 and 200 <= y <= 250:  # Close button
            game.menu_open = False
            game.sound_manager.play_sfx("button", volume=1.0)
        elif 400 <= x <= 600 and 300 <= y <= 350:  # Toggle sound button
            game.sound_manager.stop_music()
            game.sound_manager.play_sfx("button", volume=1.0)
        return  # Prevent clicks from affecting the game
        


""""""


"""Handle Mouse Motion"""


""""""



def handle_mouse_motion(game, x, y, _dx, _dy, game_state):
        if game.stage == game_state.OUTSIDE:
            mouse_motion_outside(game,x,y, game_state)
        if game.stage == game_state.INTRO:
            mouse_motion_intro(game,x,y, game_state)
        if game.stage == game_state.SPREAD:
            mouse_motion_spread(game,x,y, game_state)
        if game.stage == game_state.READING_INTRO:
            mouse_motion_reading_intro(game,x,y, game_state)
        if game.stage in {
            game_state.READING_CARD_1,
            game_state.READING_CARD_2,
            game_state.READING_CARD_3,
        }:
            mouse_motion_reading_cards(game,x,y,game_state)
        if game.stage == game_state.READING_SUMMARY:
            mouse_motion_reading_summary(game,x,y,game_state)

        if game.stage != game_state.TITLE:
             mouse_motion_option_button(game, x,y, game_state)

        
        
    

def mouse_motion_outside(game,x,y,game_state):
    if game.x_middle_button - game.button_clickbox_width <= x <= game.x_middle_button + game.button_clickbox_width and \
        game.y_bottom_button <= y <= game.y_bottom_button + game.button_clickbox_height:
            game.hovered_button = "step_inside"
    
    elif (game.x_right_button + 200) - (game.button_clickbox_width // 2)  <= x <= game.x_right_button + 200 + (game.button_clickbox_width //2) and \
        game.y_bottom_button <= y <= game.y_bottom_button - 50 + (game.button_clickbox_height):
            game.hovered_button = "exit_game"
    else:
            game.hovered_button = None

def mouse_motion_intro(game,x,y,game_state):
    # Loop through button positions and detect hover
    for i, (bx, by) in enumerate([
        (275, 300),  # Button 0
        (650, 300),  # Button 1
        (1025, 300),  # Button 2
        (275, 150),  # Button 3
        (650, 150),  # Button 4
        (1025, 150)  # Button 5
    ]):
        # Check if the mouse is within the button's bounds
        if bx - game.button_clickbox_width <= x <= bx + game.button_clickbox_width and by - 50 <= y <= by + 100:
            game.hovered_button = f"button_{i}"
            break
        else:
            game.hovered_button = None

    # do reverse for topmost card

def mouse_motion_spread(game,x,y,game_state):

    if game.reveal_active and not game.start_reading_button_active:
        game.hovered_card = None  # Ensure no card is hovered when revealing
        if game.x_middle_button - game.button_clickbox_width <= x <= game.x_middle_button + game.button_clickbox_width and \
        game.y_bottom_button <= y <= game.y_bottom_button + game.button_clickbox_height:
            game.hovered_button = "pull_next"
        else:
            game.hovered_button = None  # Reset hover state if not within bounds
        return
    elif game.reveal_active and game.start_reading_button_active:
        game.hovered_card = None
        if game.x_middle_button - game.button_clickbox_width <= x <= game.x_middle_button + game.button_clickbox_width and \
        game.y_bottom_button <= y <= game.y_bottom_button + game.button_clickbox_height:
            game.hovered_button = "begin_reading"

        else:
            game.hovered_button = None  # Reset hover state if not within bounds
        return
# Normal hover behavior
    game.hovered_card = None
    game.hovered_button = None

    for card in reversed(game.deck.cards):
        if card.is_clicked(x, y): 
            game.hovered_card = card
            break


def mouse_motion_reading_intro(game,x,y,game_state):
    if game.x_middle_button - game.button_clickbox_width <= x <= game.x_middle_button + game.button_clickbox_width and \
        game.y_bottom_button <= y <= game.y_bottom_button + game.button_clickbox_height:
            game.hovered_button = "next_card"
    else:
         game.hovered_button = None
def mouse_motion_reading_cards(game,x,y,game_state):
    if game.x_left_button - game.button_clickbox_width <= x <= game.x_left_button + game.button_clickbox_width and \
        game.y_bottom_button <= y <= game.y_bottom_button + game.button_clickbox_height:
            game.hovered_button = "previous_card"
   
    elif game.x_right_button - game.button_clickbox_width <= x <= game.x_right_button + game.button_clickbox_width and \
        game.y_bottom_button <= y <= game.y_bottom_button + game.button_clickbox_height:
            game.hovered_button = "next_card"
    else:
         game.hovered_button = None        
def mouse_motion_reading_summary(game,x,y,game_state):
    if game.x_middle_button - game.button_clickbox_width <= x <= game.x_middle_button + game.button_clickbox_width and \
        game.y_bottom_button <= y <= game.y_bottom_button + game.button_clickbox_height:
            game.hovered_button = "new_reading"
    
    elif game.x_left_button - 100 - game.button_clickbox_width <= x <= game.x_left_button- 100 + game.button_clickbox_width and \
        game.y_bottom_button <= y <= game.y_bottom_button + game.button_clickbox_height:
            game.hovered_button = "previous_card"
  
    elif game.x_right_button+100 - game.button_clickbox_width <= x <= game.x_right_button+100 + game.button_clickbox_width and \
        game.y_bottom_button <= y <= game.y_bottom_button + game.button_clickbox_height:
            game.hovered_button = "go_outside"
    else:
         game.hovered_button = None
    # Check if hovering over "Begin Reading" button

def mouse_motion_option_button(game, x, y, game_state):
    if game.x_right_button + 250 - 100 <= x <= game.x_right_button + 250 + 100 and \
            900-20 <= y <= 900 - 50 + 100:
        
        game.hovered_button = "options"
    
    
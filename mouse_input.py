from enum import Enum
from game import CATEGORIES


""" Handle Mouse Clicks"""

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



def mouse_press_outside(game, x, y, game_state):
    print(f"Mouse clicked at ({x}, {y})")
    print(f"game_state is {game.stage}")
    if game.x_right_button + 200 - game.button_clickbox_width // 2 <= x <= game.x_right_button + 200 + game.button_clickbox_width // 2 and \
            game.y_bottom_button <= y <= game.y_bottom_button - 50 + game.button_clickbox_height:
        game.close()
        return
    if game.x_middle_button - game.button_clickbox_width <= x <= game.x_middle_button + game.button_clickbox_width and \
            game.y_bottom_button <= y <= game.y_bottom_button + game.button_clickbox_height:
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
                if bx - game.button_clickbox_width <= x <= bx + game.button_clickbox_width and by <= y <= by + game.button_clickbox_height:  # Button bounds
                    game.clicked_button = f"button_{i}"
                    game.set_intention(CATEGORIES[i])  # Set intention based on button index
                    return
                

def mouse_press_spread(game, x, y, _game_state):
            if game.reveal_active:
                if game.x_middle_button - game.button_clickbox_width <= x <= game.x_middle_button + game.button_clickbox_width and game.y_bottom_button  <= y <= game.y_bottom_button  + game.button_clickbox_height:
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
        game.stage = game_state.INTRO
    if game.x_left_button - 100 - game.button_clickbox_width <= x <= game.x_left_button- 100 + game.button_clickbox_width and \
        game.y_bottom_button <= y <= game.y_bottom_button + game.button_clickbox_height:
        previous_reading_stage(game, game_state)
        return
    if game.x_right_button+100 - game.button_clickbox_width <= x <= game.x_right_button+100 + game.button_clickbox_width and \
        game.y_bottom_button <= y <= game.y_bottom_button + game.button_clickbox_height:
        game.reset_data()
        game.stage = game_state.OUTSIDE


def advance_reading_stage(game, game_state):
        """ Advance to the next reading stage. """
        if game.stage == game_state.READING_INTRO:
            game.stage = game_state.READING_CARD_1
        elif game.stage == game_state.READING_CARD_1:
            game.stage = game_state.READING_CARD_2
        elif game.stage == game_state.READING_CARD_2:
            game.stage = game_state.READING_CARD_3
        elif game.stage == game_state.READING_CARD_3:
            game.stage = game_state.READING_SUMMARY
        elif game.stage == game_state.READING_SUMMARY:
            print("Reading complete.")  # Placeholder for post-reading action

def previous_reading_stage(game, game_state):
    """Return to previous reading stage"""
    if game.stage == game_state.READING_CARD_1:
        game.stage = game_state.READING_INTRO
    elif game.stage == game_state.READING_CARD_2:
        game.stage = game_state.READING_CARD_1
    elif game.stage == game_state.READING_CARD_3:
        game.stage = game_state.READING_CARD_2
    elif game.stage == game_state.READING_SUMMARY:
        game.stage = game_state.READING_CARD_3
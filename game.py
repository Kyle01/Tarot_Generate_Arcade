import arcade
import threading
import pyglet
import textwrap
import draw_utility
from deck import TarotDeck
from tarot_bot import TarotBot
from enum import Enum

# Screen title and size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
DEFAULT_LINE_HEIGHT = 24
DEFAULT_FONT_SIZE = 16
FONT_PATH = r"assets/fonts/OldSchoolAdventures-42j9.ttf"

CATEGORIES = ["Love Life", "Professional Development", "Family and Friends", "Health", "Personal Growth", "Gain Clarity"]

class GameState(Enum):
    OUTSIDE =1
    INTRO = 2
    SPREAD = 3
    LOADING = 4
    READING_INTRO = 5
    READING_CARD_1 = 6
    READING_CARD_2 = 7
    READING_CARD_3 = 8
    READING_SUMMARY = 9

class TarotGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Voodoo Tarot GPT")
        self.tarot_bot = TarotBot()
        self.stage = GameState.OUTSIDE
        self.intention = None
        self.drawn_cards = None
        self.fortune = None
        self.hovered_card = None
        self.hovered_button = None  # Track which button is hovered
        self.clicked_button = None  # Track which button is clicked
        self.current_revealed_card = None
        self.reveal_active= False
        self.start_reading_button_active = False
        self.background_image = arcade.load_texture("assets/original/TableClothbigger.png")
        self.outside_image = arcade.set_background_color(arcade.color.IMPERIAL_PURPLE) ## replace with cover art
        self.frame_timer = 0
        self.frame_rate = 0.4
        self.button_texture = arcade.load_texture("assets/original/Purple Button Big.png")
        self.button_pressed_texture = arcade.load_texture("assets/original/Purple Button Pressed Big.png")
        arcade.set_background_color(arcade.color.IMPERIAL_PURPLE)
       
      
        pyglet.font.add_file(FONT_PATH)  # Load the font file
           
        self.button_clickbox_width = 175
        self.button_clickbox_height = 150
        self.x_middle_button = SCREEN_WIDTH // 2
        self.x_left_button = SCREEN_WIDTH // 4
        self.x_right_button = SCREEN_WIDTH * .75
        self.y_bottom_button = 25
        

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        pass

    def reset_data(self):
        self.intention = None
        self.drawn_cards = None
        self.fortune = None
        self.hovered_card = None
        self.hovered_button = None  # Track which button is hovered
        self.clicked_button = None  # Track which button is clicked
        self.current_revealed_card = None
        self.reveal_active= False
        self.start_reading_button_active = False

    def on_draw(self):
        """ Render the screen. """
        self.clear()

        if self.stage != GameState.OUTSIDE:
            arcade.draw_lrwh_rectangle_textured(0,0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_image)
        if self.stage == GameState.OUTSIDE:
            arcade.set_background_color(arcade.color.IMPERIAL_PURPLE)
            draw_utility.outside_stage(self)
        elif self.stage == GameState.INTRO:
            draw_utility.draw_intro_stage(self)
        elif self.stage == GameState.SPREAD:
            draw_utility.draw_spread_stage(self)
        elif self.stage == GameState.LOADING:
            draw_utility.draw_loading_stage(self)
        elif self.stage == GameState.READING_INTRO:
            draw_utility.draw_reading_intro(self) # Stage 1: Show all cards and intro
        elif self.stage == GameState.READING_CARD_1:
            draw_utility.draw_reading_card(self, 1)  # Stage 2: Show card 1
        elif self.stage == GameState.READING_CARD_2:
            draw_utility.draw_reading_card(self, 2)  # Stage 3: Show card 2
        elif self.stage == GameState.READING_CARD_3:
            draw_utility.draw_reading_card(self, 3)  # Stage 4: Show card 3
        elif self.stage == GameState.READING_SUMMARY:
            draw_utility.draw_reading_summary(self)  # Stage 5: Show all cards and summary
            

        '''For Debugging Hit boxes'''
        # hitbox_x = self.x_right_button + 200
        # hitbox_y = self.y_bottom_button - 50 + (self.button_clickbox_height // 4)  # Center the y-coordinate
        # hitbox_width = self.button_clickbox_width
        # hitbox_height = self.button_clickbox_height // 2

        # 
        # arcade.draw_rectangle_outline(
        #     center_x=hitbox_x,
        #     center_y=hitbox_y,
        #     width=hitbox_width,
        #     height=hitbox_height,
        #     color=arcade.color.RED,  # Red color for visibility
        #     border_width=2
        # )
    def on_mouse_press(self, x, y, _button, _key_modifiers):
        
        
        def mouse_press_outside(x,y):
            if (self.x_right_button + 200) - (self.button_clickbox_width // 2)  <= x <= self.x_right_button + 200 + (self.button_clickbox_width //2) and \
                self.y_bottom_button <= y <= self.y_bottom_button - 50 + (self.button_clickbox_height):
                arcade.close_window()
                return
            if self.x_middle_button - self.button_clickbox_width <= x <= self.x_middle_button + self.button_clickbox_width and self.y_bottom_button <= y <= self.y_bottom_button +self.button_clickbox_height:
                self.stage = GameState.INTRO
                return
        def mouse_press_intro(x, y):
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
                if bx - self.button_clickbox_width <= x <= bx + self.button_clickbox_width and by <= y <= by + self.button_clickbox_height:  # Button bounds
                    self.clicked_button = f"button_{i}"
                    self.set_intention(CATEGORIES[i])  # Set intention based on button index
                    return
            
        def mouse_press_spread(x,y):
            if self.reveal_active:
                if self.x_middle_button - self.button_clickbox_width <= x <= self.x_middle_button + self.button_clickbox_width and self.y_bottom_button  <= y <= self.y_bottom_button  + self.button_clickbox_height:
                    # Dismiss popup and place the revealed card in the corner
                    self.reveal_active = False
    
                    self.current_revealed_card = None
                    if len(self.selected_cards) == 2:
                        self.start_reading_button_active = True
                        print(f"is start reading active: {self.start_reading_button_active}")
                    if len(self.selected_cards) == 3:
                        self.drawn_cards = self.selected_cards
                        self.start_loading()
                        self.start_reading_button_active = False
                        print(f"is start reading active: {self.start_reading_button_active}")
                    return
                    
        
            if not self.reveal_active:
                for card in reversed(self.deck.cards):
                    if card.is_clicked(x, y):
                        self.deck.cards.remove(card)
                        self.reveal_card(card) 
                        # Trigger popup for selected card
                        return
                    
        def mouse_press_reading_intro(x,y):
            
            if self.x_middle_button-self.button_clickbox_width <= x <= self.x_middle_button + self.button_clickbox_width and self.y_bottom_button <= y <= self.y_bottom_button + self.button_clickbox_height:
                self.advance_reading_stage()
                return
            

        
        def mouse_press_reading_cards(x,y):
                        
            if self.x_right_button-self.button_clickbox_width <= x <= self.x_right_button + self.button_clickbox_width and self.y_bottom_button  <= y <= self.y_bottom_button + self.button_clickbox_height:
                self.advance_reading_stage()
                return
            if self.x_left_button - self.button_clickbox_width <= x <= self.x_left_button + self.button_clickbox_width and self.y_bottom_button <= y <= self.y_bottom_button +self.button_clickbox_height:
                self.previous_reading_stage()
                return
        
        def mouse_press_reading_summary(x,y):
          
            
            
            if self.x_middle_button - self.button_clickbox_width <= x <= self.x_middle_button + self.button_clickbox_width and self.y_bottom_button  <= y <= self.y_bottom_button +self.button_clickbox_height:
                self.reset_data()
                self.stage = GameState.INTRO
            if self.x_left_button - 100 - self.button_clickbox_width <= x <= self.x_left_button- 100 + self.button_clickbox_width and \
                self.y_bottom_button <= y <= self.y_bottom_button + self.button_clickbox_height:
                self.previous_reading_stage()
                return
            if self.x_right_button+100 - self.button_clickbox_width <= x <= self.x_right_button+100 + self.button_clickbox_width and \
                self.y_bottom_button <= y <= self.y_bottom_button + self.button_clickbox_height:
                self.reset_data()
                self.stage = GameState.OUTSIDE



        if self.stage == GameState.OUTSIDE:
            mouse_press_outside(x,y)
        elif self.stage == GameState.INTRO:
            mouse_press_intro(x,y)
        elif self.stage == GameState.SPREAD:
            mouse_press_spread(x,y)
        elif self.stage == GameState.READING_INTRO:
            mouse_press_reading_intro(x,y)
        elif self.stage in {
            GameState.READING_CARD_1,
            GameState.READING_CARD_2,
            GameState.READING_CARD_3,
        }:
            mouse_press_reading_cards(x,y)
        elif self.stage == GameState.READING_SUMMARY:
            mouse_press_reading_summary(x,y)

    def advance_reading_stage(self):
        """ Advance to the next reading stage. """
        if self.stage == GameState.READING_INTRO:
            self.stage = GameState.READING_CARD_1
        elif self.stage == GameState.READING_CARD_1:
            self.stage = GameState.READING_CARD_2
        elif self.stage == GameState.READING_CARD_2:
            self.stage = GameState.READING_CARD_3
        elif self.stage == GameState.READING_CARD_3:
            self.stage = GameState.READING_SUMMARY
        elif self.stage == GameState.READING_SUMMARY:
            print("Reading complete.")  # Placeholder for post-reading action

    def previous_reading_stage(self):
        """Return to previous reading stage"""
        if self.stage == GameState.READING_CARD_1:
            self.stage = GameState.READING_INTRO
        elif self.stage == GameState.READING_CARD_2:
            self.stage = GameState.READING_CARD_1
        elif self.stage == GameState.READING_CARD_3:
            self.stage = GameState.READING_CARD_2
        elif self.stage == GameState.READING_SUMMARY:
            self.stage = GameState.READING_CARD_3
        
    
    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle mouse movement to track hovered card. """
        self.hovered_card = None  

        self.hovered_button = None

        def mouse_motion_outside(x,y):
            if self.x_middle_button - self.button_clickbox_width <= x <= self.x_middle_button + self.button_clickbox_width and \
                self.y_bottom_button <= y <= self.y_bottom_button + self.button_clickbox_height:
                    self.hovered_button = "step_inside"
            if (self.x_right_button + 200) - (self.button_clickbox_width // 2)  <= x <= self.x_right_button + 200 + (self.button_clickbox_width //2) and \
                self.y_bottom_button <= y <= self.y_bottom_button - 50 + (self.button_clickbox_height):
                    self.hovered_button = "exit_game"

        def mouse_motion_intro(x,y):
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
                if bx - self.button_clickbox_width <= x <= bx + self.button_clickbox_width and by - 100 <= y <= by + 100:
                    self.hovered_button = f"button_{i}"
                    break

            # do reverse for topmost card

        def mouse_motion_spread(x,y):

            if self.reveal_active and not self.start_reading_button_active:
                self.hovered_card = None  # Ensure no card is hovered when revealing
                if self.x_middle_button - self.button_clickbox_width <= x <= self.x_middle_button + self.button_clickbox_width and \
                self.y_bottom_button <= y <= self.y_bottom_button + self.button_clickbox_height:
                    self.hovered_button = "pull_next"
                else:
                    self.hovered_button = None  # Reset hover state if not within bounds
                return
            elif self.reveal_active and self.start_reading_button_active:
                self.hovered_card = None
                if self.x_middle_button - self.button_clickbox_width <= x <= self.x_middle_button + self.button_clickbox_width and \
                self.y_bottom_button <= y <= self.y_bottom_button + self.button_clickbox_height:
                    self.hovered_button = "begin_reading"

                else:
                    self.hovered_button = None  # Reset hover state if not within bounds
                return
        # Normal hover behavior
            self.hovered_card = None
            self.hovered_button = None

            for card in reversed(self.deck.cards):
                if card.is_clicked(x, y): 
                    self.hovered_card = card
                    break
        

        def mouse_motion_reading_intro(x,y):
            if self.x_middle_button - self.button_clickbox_width <= x <= self.x_middle_button + self.button_clickbox_width and \
                self.y_bottom_button <= y <= self.y_bottom_button + self.button_clickbox_height:
                    self.hovered_button = "next_card"
        def mouse_motion_reading_cards(x,y):
            if self.x_left_button - self.button_clickbox_width <= x <= self.x_left_button + self.button_clickbox_width and \
                self.y_bottom_button <= y <= self.y_bottom_button + self.button_clickbox_height:
                    self.hovered_button = "next_card"
            if self.x_right_button - self.button_clickbox_width <= x <= self.x_right_button + self.button_clickbox_width and \
                self.y_bottom_button <= y <= self.y_bottom_button + self.button_clickbox_height:
                    self.hovered_button = "previous_card"
        def mouse_motion_reading_summary(x,y):
            if self.x_middle_button - self.button_clickbox_width <= x <= self.x_middle_button + self.button_clickbox_width and \
                self.y_bottom_button <= y <= self.y_bottom_button + self.button_clickbox_height:
                    self.hovered_button = "new_reading"
            if self.x_left_button - 100 - self.button_clickbox_width <= x <= self.x_left_button- 100 + self.button_clickbox_width and \
                self.y_bottom_button <= y <= self.y_bottom_button + self.button_clickbox_height:
                    self.hovered_button = "previous_card"
            if self.x_right_button+100 - self.button_clickbox_width <= x <= self.x_right_button+100 + self.button_clickbox_width and \
                self.y_bottom_button <= y <= self.y_bottom_button + self.button_clickbox_height:
                    self.hovered_button = "go_outside"
        if self.stage == GameState.OUTSIDE:
            mouse_motion_outside(x,y)
        if self.stage == GameState.INTRO:
            mouse_motion_intro(x,y)
        if self.stage == GameState.SPREAD:
            mouse_motion_spread(x,y)
        if self.stage == GameState.READING_INTRO:
            mouse_motion_reading_intro(x,y)
        if self.stage in {
            GameState.READING_CARD_1,
            GameState.READING_CARD_2,
            GameState.READING_CARD_3,
        }:
            mouse_motion_reading_cards(x,y)
        if self.stage == GameState.READING_SUMMARY:
            mouse_motion_reading_summary(x,y)
            # Check if hovering over "Begin Reading" button


    def set_intention(self, intention_text):
        """ Set the intention and transition to the spread stage. """
        self.intention = intention_text
        self.stage = GameState.SPREAD
        self.selected_cards = []  # reset selected cards for spread
        self.deck = TarotDeck()  # prepare deck
        self.deck.shuffle()

    def reveal_card(self, card):
        if card not in self.selected_cards:
            self.selected_cards.append(card)  # Add the card to selected cards
        self.current_revealed_card = card  # Track the card being revealed
        self.reveal_active = True  

    def start_loading(self):
        self.stage = GameState.LOADING
        self.loading_progress = 0.0
        self.api_call_complete = False

        
        def api_call():
            self.fortune = self.tarot_bot.fortune(self.drawn_cards, self.intention)
            print(f"Raw fortune text:\n{self.fortune}")  # Debug the raw fortune

            self.api_call_complete = True
            paragraphs = self.fortune.split('\n')  # Split the fortune into paragraphs
            print(f"Split paragraphs:\n{paragraphs}")  # Debug the split paragraphs

            # Handle wrapping logic
            default_width = 40
            last_paragraph_width = 55
            last_index = len(paragraphs) -1
            wrapped_paragraphs = [
                textwrap.fill(p.strip(), width=last_paragraph_width if i == last_index else default_width)
                for i, p in enumerate(paragraphs) if p.strip()
            ]

            self.fortune = wrapped_paragraphs
            print("\n\n".join(wrapped_paragraphs))
        threading.Thread(target=api_call).start()

    def on_update(self, delta_time):
        """ Update the game state. """
        if self.stage == GameState.LOADING:
            self.frame_timer += delta_time

            if self.frame_timer >self.frame_rate *4:
                self.frame_timer -= self.frame_rate *4

            if not self.api_call_complete:
                # load progress bar with api is called
                self.loading_progress += delta_time / 5  # adjust speed
                self.loading_progress = min(self.loading_progress, 0.95)  # cap at 95%
            else:
                # finish progress bar if api is done loading first
                self.loading_progress += delta_time / 2  
                if self.loading_progress >= 1.0:
                    self.loading_progress = 1.0
                    self.stage = GameState.READING_INTRO

def main():
    """ Main function """
    window = TarotGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
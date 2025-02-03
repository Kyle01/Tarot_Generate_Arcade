import arcade
import threading
import pyglet
import draw_utility
import text_utility as TEXT
import mouse_input
from sound_manager import SoundManager
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
        self.stage = GameState.OUTSIDE

        """ Variables for reading generation"""

        self.tarot_bot = TarotBot()
        self.intention = None
        self.drawn_cards = None
        self.fortune = None

        """ Variables for spread stage"""

        self.hovered_card = None
        self.current_revealed_card = None
        self.reveal_active= False

        """ Varables for progress bar"""
        self.frame_timer = 0
        self.frame_rate = 0.4
  
        """ Global Assets """
        self.background_image = arcade.load_texture("assets/original/TableClothbigger.png")
        self.outside_image = arcade.set_background_color(arcade.color.IMPERIAL_PURPLE) ## replace with cover art
        arcade.set_background_color(arcade.color.IMPERIAL_PURPLE)
        pyglet.font.add_file(FONT_PATH)  # Load the font file
        
        """ Variables for button formatting"""

        self.start_reading_button_active = False
        self.hovered_button = None  # Track which button is hovered
        self.clicked_button = None  # Track which button is clicked
        self.button_clickbox_width = 175
        self.button_clickbox_height = 150
        self.x_middle_button = SCREEN_WIDTH // 2
        self.x_left_button = SCREEN_WIDTH // 4
        self.x_right_button = SCREEN_WIDTH * .75
        self.y_bottom_button = 25

        """ Variables for typewriter Effect """

        self.text_index = 0
        self.displayed_text =""
        self.typing_speed= .03
        self.typing_timer= 0
        self.current_text = ""
        self.current_line_index = 0
        self.lines_to_type = []
        

        """ Variables for sound"""
        self.sound_manager = SoundManager("assets\sound\Pixel 1.ogg")
        self.sound_manager.load_music()
        self.sound_manager.load_sfx("card_move", "assets\sound\JDSherbert - Tabletop Games SFX Pack - Paper Flip - 1.wav")
        self.sound_manager.load_sfx("card_spread", "assets\sound\JDSherbert - Tabletop Games SFX Pack - Deck Shuffle - 1.wav")
        self.sound_manager.load_sfx("button", "assets\sound\clonck.wav")
        self.sound_manager.load_sfx("door", "assets\sound\mixkit-creaky-door-open-195.wav")
        self.sound_manager.load_sfx("typewriter", "assets\sound\mixkit-modern-click-box-check-1120.wav")

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        
        self.sound_manager.play_music(volume = 0.6, loop=True)
        pass

    def reset_data(self):
        """ Resets the class variables for new readings """
        self.intention = None
        self.drawn_cards = None
        self.fortune = None
        self.hovered_card = None
        self.hovered_button = None  
        self.clicked_button = None 
        self.current_revealed_card = None
        self.reveal_active= False
        self.start_reading_button_active = False
        self.active_card_index = None

    def on_draw(self):
        """ Render the screen. """
        self.clear()

        if self.stage != GameState.OUTSIDE:
            arcade.draw_lrwh_rectangle_textured(0,0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_image)
        if self.stage == GameState.OUTSIDE:
            arcade.set_background_color(arcade.color.IMPERIAL_PURPLE)
            draw_utility.draw_outside_stage(self)
        elif self.stage == GameState.INTRO:
            draw_utility.draw_intro_stage(self)
        elif self.stage == GameState.SPREAD:
            draw_utility.draw_spread_stage(self)
        elif self.stage == GameState.LOADING:
            draw_utility.draw_loading_stage(self)
        elif self.stage == GameState.READING_INTRO:
            draw_utility.draw_reading_intro(self, 0) # Stage 1: Show all cards and intro
        elif self.stage == GameState.READING_CARD_1:
            draw_utility.draw_reading_card(self, 1)  # Stage 2: Show card 1
        elif self.stage == GameState.READING_CARD_2:
            draw_utility.draw_reading_card(self, 2)  # Stage 3: Show card 2
        elif self.stage == GameState.READING_CARD_3:
            draw_utility.draw_reading_card(self, 3)  # Stage 4: Show card 3
        elif self.stage == GameState.READING_SUMMARY:
            draw_utility.draw_reading_summary(self, 4),   # Stage 5: Show all cards and summary
            

        '''For Debugging Button Hit boxes'''
        # hitbox_x = self.x_right_button + 200
        # hitbox_y = self.y_bottom_button - 50 + (self.button_clickbox_height // 4)  # Center the y-coordinate
        # hitbox_width = self.button_clickbox_width
        # hitbox_height = self.button_clickbox_height // 2

        
        # arcade.draw_rectangle_outline(
        #     center_x=hitbox_x,
        #     center_y=hitbox_y,
        #     width=hitbox_width,
        #     height=hitbox_height,
        #     color=arcade.color.RED,  # Red color for visibility
        #     border_width=2
        # )
    def on_mouse_press(self, x, y, _button, _modifiers):
           
        mouse_input.handle_mouse_press(self,x,y, _button, _modifiers, GameState)
        
    def on_mouse_motion(self, x, y, dx, dy):

        mouse_input.handle_mouse_motion(self, x, y, dx, dy, GameState)
       

    def set_intention(self, intention_text):
        """ Set the intention and transition to the spread stage. """
        self.intention = intention_text
        self.deck = TarotDeck()  # prepare deck
        self.deck.shuffle()
        TEXT.reset_typing_state(self)  
        self.stage = GameState.SPREAD
        self.selected_cards = []  # reset selected cards for spread

    def reveal_card(self, card):
        if card not in self.selected_cards:
            self.selected_cards.append(card)  # Add the card to selected cards
        self.current_revealed_card = card  # Track the card being revealed
        self.reveal_active = True  

    def start_loading(self):
        self.stage = GameState.LOADING
        self.loading_progress = 0.0
        self.api_call_complete = False
        api_thread = threading.Thread(
            target=self.tarot_bot.api_call,
            args=(self, self.drawn_cards, self.intention),
            daemon=True  # Set as a daemon thread so it exits when the game exits
        )
        api_thread.start()
        self.sound_manager.play_sfx("card_spread", volume=1.0)
        

    def on_update(self, delta_time):
        """ Update the game state. """

        TEXT.update_typing_effect(self, delta_time)
        

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
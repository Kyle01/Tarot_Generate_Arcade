import arcade
import threading
import pyglet
import draw_utility
import text_utility as TEXT
import mouse_input
import random
import os
import update_manager
from dotenv import load_dotenv
from sound_manager import SoundManager
from deck import TarotDeck
from fetch_utility import get_fortune, generate_auth_headers
from enum import Enum

load_dotenv()

mode = os.environ.get('DEPLOY_MODE')

# Screen title and size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
DEFAULT_LINE_HEIGHT = 24
DEFAULT_FONT_SIZE = 16
FONT_PATH = r"assets/fonts/OldSchoolAdventures-42j9.ttf"

CATEGORIES = ["Love Life", "Professional Development", "Family and Friends", "Health", "Personal Growth", "Gain Clarity"]

class GameState(Enum):
    TITLE = 1
    OUTSIDE =2
    INTRO = 3
    SPREAD = 4
    LOADING = 5
    READING_INTRO = 6
    READING_CARD_1 = 7
    READING_CARD_2 = 8
    READING_CARD_3 = 9
    READING_SUMMARY = 10

class TarotGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Voodoo Tarot GPT")
        self.stage = GameState.OUTSIDE

        """ Variables for reading generation"""
        self.request_url = "http://127.0.0.1:5000/" if os.environ.get("DEPLOY_MODE") == "dev" else "https://tarot-generate-arcade.onrender.com/"
        self.has_tokens = True
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
        self.background_image = arcade.load_texture(r"assets/original/TableClothbiggerHueShift1.png")
        self.outside_image = arcade.load_texture("assets/original/AnimationFrames2.1/NolaHouse2.1.1.png")
        arcade.set_background_color(arcade.color.BLACK)
        pyglet.font.add_file(FONT_PATH)  # Load the font file

        """ Variables for Outside Animation"""
        self.outside_frame_center = arcade.load_texture(r"assets/original/AnimationFrames2.1/NolaHouse2.1.1.png")
        self.outside_frame_left = arcade.load_texture(r"assets/original/AnimationFrames2.1/NolaHouse2.1.3.png")
        self.outside_frame_right = arcade.load_texture(r"assets/original/AnimationFrames2.1/NolaHouse2.1.2.png")
        self.states = ["START","LEFT", "CENTER", "RIGHT", "CENTER"] # this creates the order for the animation frames, below is the timing for each
        self.state_index = 0  # start at 0 => "Start"

        # Track how long we've been in the current state
        self.time_in_state = 0.0

        # Define duration (seconds) for each state
        self.durations = {
            "LEFT": 1.2,     
            "CENTER": random.randint(6,10),  
            "RIGHT": 1.2,
            "START":2     # start center for a smaller amount to make sure users see and hear wind animation before entering house
        }

        """ Variables for button formatting"""

        self.start_reading_button_active = False
        self.hovered_button = None  # Track which button is hovered, used for mouse over highlights with the Button Class
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
        self.sound_manager = SoundManager(r"assets/sound/Pixel 1.wav")
        self.sound_manager.load_music()
        self.sound_manager.load_sfx("card_move", r"assets/sound/JDSherbert - Tabletop Games SFX Pack - Paper Flip - 1.wav")
        self.sound_manager.load_sfx("card_spread", r"assets/sound/JDSherbert - Tabletop Games SFX Pack - Deck Shuffle - 1.wav")
        self.sound_manager.load_sfx("button", r"assets/sound/clonck.wav")
        self.sound_manager.load_sfx("door", r"assets/sound/mixkit-creaky-door-open-195.wav")
        self.sound_manager.load_sfx("typewriter", r"assets/sound/mixkit-modern-click-box-check-1120.wav")
        self.sound_manager.load_sfx("wind", r"assets/sound/mixkit-storm-wind-2411.wav")

        """ Variables for Options Menu"""
        self.credits_open = False
        self.menu_open = False
        

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        
        self.sound_manager.play_music(volume = 0.6, loop=True)
        self.check_token_usage()
        print(f"DEPLOY_MODE is: {mode}")
       
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

        if self.stage not in [GameState.OUTSIDE, GameState.TITLE]:
            arcade.draw_lrwh_rectangle_textured(0,0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_image)
        if self.stage == GameState.TITLE:
            draw_utility.draw_title_stage(self)
        elif self.stage == GameState.OUTSIDE:
        
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
        
        if self.stage != GameState.TITLE:
            draw_utility.options_button(self)

        if self.menu_open:
            draw_utility.draw_options_menu(self)
        if self.credits_open:
            draw_utility.draw_credits_screen(self)

        # '''For Debugging Button Hit boxes'''
        # hitbox_x = self.x_right_button + 200
        # hitbox_y = (self.y_bottom_button +75 +  (self.button_clickbox_height)) // 2  - 5 # Middle of Y bounds
        # hitbox_width = self.button_clickbox_width
        # hitbox_height = self.button_clickbox_height


        
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
        """ Control and save faceup cards when the use selects them """
        if card not in self.selected_cards:
            self.selected_cards.append(card)  # Add the card to selected cards
        self.current_revealed_card = card  # Track the card being revealed
        self.reveal_active = True  

    def start_loading(self):
        """  Begin Loading Screen, Call API and begin threading """
        self.stage = GameState.LOADING
        self.loading_progress = 0.0
        self.api_call_complete = False
        api_thread = threading.Thread(
            target=get_fortune,
            args=(self, self.drawn_cards, self.intention),
            daemon=True  # Set as a daemon thread so it exits when the game exits
        )
        api_thread.start()
        self.sound_manager.play_sfx("card_spread")
        

    def on_update(self, delta_time):
        """ Update the game state. """

        update_manager.handle_animation(self, delta_time, game_state = GameState)



    def check_token_usage(self):
        """
        Fetches the total_cost from Flask API endpoint `/token_status`.
        """

        headers = generate_auth_headers()
        try:
            response = requests.get(f"{self.request_url}token_status", headers=headers)
            data = response.json()

            if 'total_cost' in data:
                total_cost = data['total_cost']

                if total_cost >= 4.90:
                    print(f"🚨 WARNING: Token usage is at ${total_cost:.2f}. Approaching limit!")
                    self.has_tokens = False
                else:
                    print(f"Token usage is at ${total_cost}")
                return total_cost
            else:
                print("❌ Unexpected response structure:", data)
                return None

        except Exception as e:
            print(f"❌ Failed to fetch token cost from server: {e}")
            return None


def main():
    """ Main function """
    window = TarotGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
import arcade
import threading
import pyglet
from deck import TarotDeck
from tarot_bot import TarotBot
from enum import Enum

# Screen title and size
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
DEFAULT_LINE_HEIGHT = 24
DEFAULT_FONT_SIZE = 16
FONT_PATH = r"assets\fonts\OldSchoolAdventures-42j9.ttf"


INTRO_TEXT = (
    "Ah, welcome, traveler!\n\n"
    "I am Mama Nyah, and the spirits have brought you to me for a reason.\n\n"
    "Sit, relax, and let us see what the universe whispers for you.\n\n"
    "But first, tell me—what is your intention? What does your heart seek to know, heal, or discover?\n\n"
    "Speak it, and we will find the truth together."
)

CATEGORIES = ["Love Life", "Professional Development", "Family and Friends", "Health", "Personal Growth", "Gain Clarity"]

class GameState(Enum):
    TITLE =1
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
        self.stage = GameState.INTRO
        self.intention = None
        self.drawn_cards = None
        self.fortune = None
        self.hovered_card = None
        self.hovered_button = None  # Track which button is hovered
        self.clicked_button = None  # Track which button is clicked
        self.current_revealed_card = None
        self.reveal_active= False
        self.start_reading_button_active = False
        self.background_image = arcade.load_texture("assets\original\TableClothbigger.png")
        self.frame_timer = 0
        self.frame_rate = 0.4
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

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
    
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0,0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_image)

        if self.stage == GameState.INTRO:
            self.__draw_intro_stage()
        elif self.stage == GameState.SPREAD:
            self.__draw_spread_stage()
        elif self.stage == GameState.LOADING:
            self.__draw_loading_stage()
        elif self.stage in {
            GameState.READING_INTRO,
            GameState.READING_CARD_1,
            GameState.READING_CARD_2,
            GameState.READING_CARD_3,
            GameState.READING_SUMMARY,
        }:
            self.__draw_reading_stage()  # Centralized logic for all reading sub-stages
            

    def on_mouse_press(self, x, y, _button, _key_modifiers):
        
        

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
                self.previous_reading_stage()
                return

        if self.stage == GameState.INTRO:
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

        if self.stage == GameState.INTRO:
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

        if self.stage == GameState.SPREAD:
            # do reverse for topmost card

            if self.stage == GameState.SPREAD:
    # Hover logic for topmost card
                if self.reveal_active and not self.start_reading_button_active:
                    self.hovered_card = None  # Ensure no card is hovered when revealing
                    if self.x_middle_button - self.button_clickbox_width <= x <= self.x_middle_button + self.button_clickbox_width and \
                    self.y_bottom_button <= y <= self.y_bottom_button + self.button_clickbox_height:
                        self.hovered_button = "pull_next"
                        # print(f"what is hovered: {self.hovered_button}")
                    else:
                        self.hovered_button = None  # Reset hover state if not within bounds
                    return
                elif self.reveal_active and self.start_reading_button_active:
                    self.hovered_card = None
                    if self.x_middle_button - self.button_clickbox_width <= x <= self.x_middle_button + self.button_clickbox_width and \
                    self.y_bottom_button <= y <= self.y_bottom_button + self.button_clickbox_height:
                        self.hovered_button = "begin_reading"
                        # print(f"what is hovered: {self.hovered_button}")

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
            self.api_call_complete = True

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


    def __draw_intro_stage(self):
        # Load textures
        self.button_texture = arcade.load_texture("assets/original/Purple Button Big.png")
        self.button_pressed_texture = arcade.load_texture("assets/original/Purple Button Pressed Big.png")

        # Intro text
        arcade.draw_text(
            INTRO_TEXT,
            0,
            SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 5,
            arcade.color.WHITE,
            DEFAULT_FONT_SIZE,
            width=SCREEN_WIDTH,
            multiline=True,
            align="center",
            font_name="Old School Adventures"
        )

        # Button positions
        button_positions = [
            (275, 300),  # Button 0
            (650, 300),  # Button 1
            (1025, 300),  # Button 2
            (275, 150),  # Button 3
            (650, 150),    # Button 4
            (1025, 150)     # Button 5
        ]

        # Loop through categories and draw buttons
        for i, (x, y) in enumerate(button_positions):
            button_texture = (
                self.button_pressed_texture if self.hovered_button == f"button_{i}" else self.button_texture
            )
            arcade.draw_texture_rectangle(x, y, 350, 200, button_texture)

            arcade.draw_text(
                CATEGORIES[i],
                x - 125,  # Center text
                y,   # Position text slightly below center
                arcade.color.WHITE,
                DEFAULT_FONT_SIZE,
                width=250,
                align="center",
                font_name="Old School Adventures"
            )


    def __draw_reading_stage(self):


        if self.stage == GameState.READING_INTRO:
            self._draw_reading_intro()  # Stage 1: Show all cards and intro

        elif self.stage == GameState.READING_CARD_1:
            self._draw_reading_card(1)  # Stage 2: Show card 1

        elif self.stage == GameState.READING_CARD_2:
            self._draw_reading_card(2)  # Stage 3: Show card 2

        elif self.stage == GameState.READING_CARD_3:
            self._draw_reading_card(3)  # Stage 4: Show card 3

        elif self.stage == GameState.READING_SUMMARY:
            self._draw_reading_summary()  # Stage 5: Show all cards and summary

    def _draw_reading_intro(self):
        """ Render the intro stage with all cards shown. """
        # Placeholder logic
        arcade.draw_text(
            "Welcome to your reading. Here are your cards:",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 50,
            arcade.color.WHITE,
            font_size=24,
            anchor_x="center"
        )

        arcade.draw_texture_rectangle(
            self.x_middle_button,
            100,
            350,
            200,
            self.button_texture)
        
        arcade.draw_text(
                    "Next Card",
                    self.x_middle_button - 125,
                    85,
                    arcade.color.WHITE,
                    DEFAULT_FONT_SIZE,
                    width=250,
                    align="center",
                    font_name="Old School Adventures"
                )

        for i, card in enumerate(self.drawn_cards):
            x = 350 + (i * 275)
            y = 400
            card.paint(x, y, show_front=True)

    def _draw_reading_card(self, card_index):
        """ Render a single card stage. """
        # Placeholder logic for displaying one card
        arcade.draw_text(
            f"Focusing on card {card_index}:",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 50,
            arcade.color.WHITE,
            font_size=24,
            anchor_x="center"
        )
        card = self.drawn_cards[card_index - 1]  # Cards are 0-indexed
        card.paint(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, show_front=True)

        arcade.draw_texture_rectangle(
            self.x_right_button,
            100,
            350,
            200,
            self.button_texture)
        
        arcade.draw_text(
                    "Next Card",
                    self.x_right_button - 125,
                    85,
                    arcade.color.WHITE,
                    DEFAULT_FONT_SIZE,
                    width=250,
                    align="center",
                    font_name="Old School Adventures"
                )
        
        arcade.draw_texture_rectangle(
            self.x_left_button,
            100,
            350,
            200,
            self.button_texture)
        
        arcade.draw_text(
                    "Previous",
                    self.x_left_button - 125,
                    85,
                    arcade.color.WHITE,
                    DEFAULT_FONT_SIZE,
                    width=250,
                    align="center",
                    font_name="Old School Adventures"
                )

    def _draw_reading_summary(self):
        """ Render the summary stage with all cards and a summary. """
        # Placeholder logic
        arcade.draw_text(
            "Your reading is complete. Here's a summary:",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 50,
            arcade.color.WHITE,
            font_size=24,
            anchor_x="center"
        )

        arcade.draw_texture_rectangle(
            self.x_middle_button,
            100,
            350,
            200,
            self.button_texture)
        
        arcade.draw_text(
                    "Previous",
                    self.x_middle_button - 125,
                    85,
                    arcade.color.WHITE,
                    DEFAULT_FONT_SIZE,
                    width=250,
                    align="center",
                    font_name="Old School Adventures"
                )

        for i, card in enumerate(self.drawn_cards):
            x = 350 + (i * 275)
            y = 400
            card.paint(x, y, show_front=True)
        for i, card in enumerate(self.drawn_cards):
            x = 350 + (i * 275)
            y = 400
            card.paint(x, y, show_front=True)


        # arcade.draw_text("Cards:",
        #         100,
        #         SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 1.5,
        #         arcade.color.WHITE,
        #         DEFAULT_FONT_SIZE,
        #         width=500,
        #         align="left")
            
        # for i, card in enumerate(self.drawn_cards):
        #     card.paint(150 + (i * 300), 550, show_front = True)

        # arcade.draw_text("Fortune:",
        #                 100,
        #                 400,
        #                 arcade.color.WHITE,
        #                 DEFAULT_FONT_SIZE,
        #                 width=500,
        #                 align="left")
        
        # arcade.draw_text(self.fortune,
        #                 100,
        #                 350,
        #                 arcade.color.WHITE,
        #                 DEFAULT_FONT_SIZE / 1.5,
        #                 multiline=True,
        #                 width=SCREEN_WIDTH - 100,
        #                 align="left")


    def __draw_loading_stage(self):
        """ Render the loading screen. """

        # Draw Loading Text
        arcade.draw_text(
            "Loading, please wait...",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 4,
            arcade.color.WHITE,
            DEFAULT_FONT_SIZE * 1.5,
            width=SCREEN_WIDTH,
            align="center",
            anchor_x="center",
            font_name="Old School Adventures"
        )

        # Progress bar dimensions
        bar_x = 100  # Starting x position of the bar
        bar_y = 300  # y position of the bar
        bar_height = 65  # Height of the progress bar
        cap_width = 35
        total_bar_width = 1050  # Total width of the progress bar background
        progress_width = self.loading_progress * (total_bar_width-50)  # Dynamic width of the stretchable section
        frame_width = 3296 //4
        frame_height = 68


        progress_bar_sprites = arcade.load_spritesheet(
                "assets\original\pBarBackgroundSpriteSheet.png",  # Path to the sprite sheet
                sprite_width=frame_width,  # Width of each frame
                sprite_height=frame_height,  # Height of each frame
                columns=4,  # Number of columns in the sprite sheet
                count=4  # Total number of frames
            )
        
        frame_index = int(self.frame_timer // self.frame_rate) % 4 

        # Load textures
        background_texture = arcade.load_texture("assets/original/pBarBackground.png")
        stretch_texture = arcade.load_texture("assets/original/pBarStretch.png")
        front_texture = arcade.load_texture("assets/original/pBarFront.png")
        end_texture = arcade.load_texture("assets/original/pBarEnd.png")

        arcade.draw_texture_rectangle(
            bar_x + total_bar_width // 2,  # Centered at the current progress width
            bar_y + bar_height // 2,
            total_bar_width,  # Dynamic width
            bar_height,
            progress_bar_sprites[frame_index]  # Use the correct frame
        )
        # Draw the static background
        arcade.draw_texture_rectangle(
            bar_x + total_bar_width // 2,  # Centered horizontally
            bar_y + bar_height // 2,  # Centered vertically
            total_bar_width,  # Full width
            bar_height,  # Full height
            background_texture
        )

        progress_width = self.loading_progress * (total_bar_width - 50)  # Dynamic width

        arcade.draw_texture_rectangle(
            bar_x+25,  # At the end of the progress bar
            bar_y + bar_height // 4 + 15,
            cap_width,  # Width of the front cap
            bar_height -10,
            front_texture
        )
        arcade.draw_texture_rectangle(
            bar_x + progress_width + cap_width / 2,  # Position at the end of the progress
            bar_y + bar_height // 2,
            cap_width,  # Width of the end cap
            bar_height-10,
            end_texture)

        # Draw the stretchable section of the progress bar
        current_x = bar_x  # Start position for the stretchable section
        while current_x +25 < bar_x + progress_width:  # Leave space for the front cap
            arcade.draw_texture_rectangle(
                current_x+cap_width,  # Centered segment
                bar_y + bar_height // 2,
                15,  # Width of each segment
                bar_height-10,
                stretch_texture
            )
            current_x += 10  # Move to the next segment


        # Draw Additional Text
        arcade.draw_text(
            "Please hold on while we prepare your reading...",
            SCREEN_WIDTH // 2,
            200,
            arcade.color.WHITE,
            DEFAULT_FONT_SIZE,
            width=SCREEN_WIDTH - 200,
            align="center",
            anchor_x="center",
            font_name="Old School Adventures"
        )

        # Draw the selected cards
        for i, card in enumerate(self.drawn_cards):
            x = 350 + (i * 275)  # Spaced out horizontally
            y = 575  # Fixed y-coordinate
            card.paint(x, y, show_front=True,scale=2.2, is_small=True)


    def __draw_spread_stage(self):
        """ Render the card spread stage with the backs of the cards. """
        if self.reveal_active and self.current_revealed_card:
            # Draw the revealed card in the center
            self.current_revealed_card.paint(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, show_front=True, scale=1.8, is_small=False)

            if len(self.selected_cards) <= 2:
                    # print(f"what is hovered: {self.hovered_button}")
                   
                    button_texture = (
                        self.button_pressed_texture if self.hovered_button == "pull_next" else self.button_texture
                    )
                    button_text = "Pull Next Card"
            else:
                    # print(f"what is hovered: {self.hovered_button}")
                    
                    button_texture = (
                        self.button_pressed_texture if self.hovered_button == "begin_reading" else self.button_texture
                    )
                    button_text = "Begin Reading"

            arcade.draw_texture_rectangle(self.x_middle_button, 100, 350, 200, button_texture)

            arcade.draw_text(
                    button_text,
                    self.x_middle_button - 125,
                    85,
                    arcade.color.WHITE,
                    DEFAULT_FONT_SIZE,
                    width=250,
                    align="center",
                    font_name="Old School Adventures"
                )
            
            arcade.draw_text(
                f"{self.current_revealed_card.name}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 4.5,
                arcade.color.WHITE,
                DEFAULT_FONT_SIZE * 1.8,
                width=SCREEN_WIDTH,
                align="center",
                anchor_x="center",
                font_name="Old School Adventures"
            )

            if len(self.selected_cards) >1 and self.selected_cards[1]:

                x = 300 
                y = 200  
                self.selected_cards[0].paint(x, y, show_front=True, is_small=True)
            
            if len(self.selected_cards) > 2 and self.selected_cards[2]:

                x=975
                y=200
                self.selected_cards[1].paint(x,y,show_front=True, is_small = True)

            return  # Stop drawing the rest of the stage while reveal is active


        # Draw instruction text
        arcade.draw_text(
            "Choose 3 Cards:",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 4.5,
            arcade.color.WHITE,
            DEFAULT_FONT_SIZE *1.5,
            width=SCREEN_WIDTH,
            align="center",
            anchor_x="center",
            font_name="Old School Adventures"
        )

        # Draw the cards
        card_spacing = (SCREEN_WIDTH - 300) // len(self.deck.cards)  # Dynamic spacing
        for i, card in enumerate(self.deck.cards):
            x = 150 + (i * card_spacing)
            y = SCREEN_HEIGHT // 2
            card.paint(x, y, show_front=False, is_hovered=(card == self.hovered_card), is_small=True)

        # Draw previously selected cards in the left corner
        for i, card in enumerate(self.selected_cards):
            x = 300 + (i * 675)  # Spaced out horizontally with 150 pixels between cards
            y = 200  # Fixed y-coordinate for all cards
            card.paint(x, y, show_front=True, is_small=True)

       



        


def main():
    """ Main function """
    window = TarotGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
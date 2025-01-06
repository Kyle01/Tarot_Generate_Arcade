import arcade
import threading
from deck import TarotDeck
from tarot_bot import TarotBot
from enum import Enum

# Screen title and size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
DEFAULT_LINE_HEIGHT = 24
DEFAULT_FONT_SIZE = 16

INTRO_TEXT = "Ah, welcome, traveler! I am Mama Nyah, and the spirits have brought you to me for a reason. Sit, relax, and let us see what the universe whispers for you. But first, tell me—what is your intention? What does your heart seek to know, heal, or discover? Speak it, and we will find the truth together."
CATEGORIES = ["Love Life", "Professional Development"]

class GameState(Enum):
    INTRO = 1,
    DRAWN = 2,
    LOADING = 3

class TarotGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Voodoo Tarot GPT")
        self.tarot_bot = TarotBot()
        self.stage = GameState.INTRO
        self.intention = None
        self.drawn_cards = None
        self.fortune = None
        

        arcade.set_background_color(arcade.color.IMPERIAL_PURPLE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        pass

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
    
        self.clear()

        if self.stage == GameState.INTRO:
            self.__draw_intro_stage()
        elif self.stage == GameState.DRAWN:
            self.__draw_drawn_stage()
        elif self.stage == GameState.LOADING:
            self.__draw_loading_stage()
            

    def on_mouse_press(self, x, y, _button, _key_modifiers):
        if self.stage == GameState.INTRO and x > 100 and x < 450 and y > 100 and y < 200:
            self.set_intention(CATEGORIES[0])
            return 
        if self.stage == GameState.INTRO and x > 600 and x < 950 and y > 100 and y < 200:
            self.set_intention(CATEGORIES[1])
            return
        pass

    def set_intention(self, intention_text):
        """ Set the intention and transition to the loading screen. """
        self.intention = intention_text
        self.stage = GameState.LOADING
        self.loading_progress = 0.0
        self.api_call_complete = False  # track api call

        # get the deck rdy for Drawn stage
        self.deck = TarotDeck()
        self.deck.shuffle()
        self.drawn_cards = self.deck.draw(3)

        # start api call as thread
        
        def api_call():
            self.fortune = self.tarot_bot.fortune(self.drawn_cards, self.intention)
            self.api_call_complete = True

        threading.Thread(target=api_call).start()


    def on_update(self, delta_time):
        """ Update the game state. """
        if self.stage == GameState.LOADING:
            if not self.api_call_complete:
                # load progress bar with api is called
                self.loading_progress += delta_time / 5  # adjust speed
                self.loading_progress = min(self.loading_progress, 0.95)  # cap at 95%
            else:
                # finish progress bar if api is done loading first
                self.loading_progress += delta_time / 2  
                if self.loading_progress >= 1.0:
                    self.loading_progress = 1.0
                    self.stage = GameState.DRAWN


    def __draw_intro_stage(self):
        arcade.draw_text(INTRO_TEXT,
                            0,
                            SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 1.5,
                            arcade.color.WHITE,
                            DEFAULT_FONT_SIZE,
                            width=SCREEN_WIDTH,
                            multiline=True,
                            align="center")
            
        arcade.draw_lrtb_rectangle_filled(100, 
                                        450, 
                                        200, 
                                        100,
                                        arcade.color.IMPERIAL_BLUE)
        arcade.draw_lrtb_rectangle_filled(125, 
                                        425, 
                                        175, 
                                        125,
                                    arcade.color.INCHWORM)
        
        arcade.draw_text(CATEGORIES[0],
                        125,
                        145,
                        arcade.color.BLACK,
                        DEFAULT_FONT_SIZE,
                        width=250,
                        align="center")
        
        arcade.draw_lrtb_rectangle_filled(600, 
                                        950, 
                                        200, 
                                        100,
                                        arcade.color.IMPERIAL_BLUE)
        arcade.draw_lrtb_rectangle_filled(625, 
                                        925, 
                                        175, 
                                        125,
                                    arcade.color.INCHWORM)
        
        arcade.draw_text(CATEGORIES[1],
                        625,
                        145,
                        arcade.color.BLACK,
                        DEFAULT_FONT_SIZE,
                        width=300,
                        align="center")

    def __draw_drawn_stage(self):
        arcade.draw_text("Cards:",
                100,
                SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 1.5,
                arcade.color.WHITE,
                DEFAULT_FONT_SIZE,
                width=500,
                align="left")
            
        for i, card in enumerate(self.drawn_cards):
            card.paint(150 + (i * 300), 550)

        arcade.draw_text("Fortune:",
                        100,
                        400,
                        arcade.color.WHITE,
                        DEFAULT_FONT_SIZE,
                        width=500,
                        align="left")
        
        arcade.draw_text(self.fortune,
                        100,
                        350,
                        arcade.color.WHITE,
                        DEFAULT_FONT_SIZE / 1.5,
                        multiline=True,
                        width=SCREEN_WIDTH - 100,
                        align="left")


    def __draw_loading_stage(self):
        """ Render the loading screen. """
       
        arcade.draw_text(
            "Loading, please wait...",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 2,
            arcade.color.WHITE,
            DEFAULT_FONT_SIZE,
            width=SCREEN_WIDTH,
            align="center",
            anchor_x="center"
        )
        
    
        arcade.draw_lrtb_rectangle_filled(
            200, 
            800, 
            300, 
            250, 
            arcade.color.IMPERIAL_BLUE
        )
        
        
        progress_width = 200 + (self.loading_progress * 600)  # Scales from 200 to 800
        arcade.draw_lrtb_rectangle_filled(
            200, 
            progress_width, 
            300, 
            250, 
            arcade.color.INCHWORM
        )
        
       
        arcade.draw_text(
            "Please hold on while we prepare your reading...",
            SCREEN_WIDTH // 2,
            200,
            arcade.color.WHITE,
            DEFAULT_FONT_SIZE / 1.5,
            width=SCREEN_WIDTH - 200,
            align="center",
            anchor_x="center"
        )



def main():
    """ Main function """
    window = TarotGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
import arcade
from deck import TarotDeck

# Screen title and size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
DEFAULT_LINE_HEIGHT = 24
DEFAULT_FONT_SIZE = 16

INTRO_TEXT = "Ah, welcome, traveler! I am Mama Nyah, and the spirits have brought you to me for a reason. Sit, relax, and let us see what the universe whispers for you. But first, tell me—what is your intention? What does your heart seek to know, heal, or discover? Speak it, and we will find the truth together."
CATEGORIES = ["Love Life", "Professional Development"]
STAGE = ['INTRO', 'PENDING', 'DRAWN']

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Voodoo Tarot GPT")
        self.stage = STAGE[0]
        self.intension = None
        self.drawn_cards = None

        arcade.set_background_color(arcade.color.IMPERIAL_PURPLE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        pass

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        if self.stage == STAGE[2]:
            arcade.draw_text("Cards:",
                            100,
                            SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 1.5,
                            arcade.color.WHITE,
                            DEFAULT_FONT_SIZE,
                            width=500,
                            align="left")
            
            for i, card in enumerate(self.drawn_cards):
                arcade.draw_text(f"{i+1}:{str(card)}",
                            100,
                            SCREEN_HEIGHT - (i + 1) * 75,
                            arcade.color.WHITE,
                            DEFAULT_FONT_SIZE,
                            width=300,
                            align="left")

            arcade.draw_text("Fortune:",
                            100,
                            400,
                            arcade.color.WHITE,
                            DEFAULT_FONT_SIZE,
                            width=500,
                            align="left")

        else: 
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

    def on_mouse_press(self, x, y, _button, _key_modifiers):
        if self.stage == STAGE[0] and x > 100 and x < 450 and y > 100 and y < 200:
            self.set_intension(CATEGORIES[0])
            return 
        if self.stage == STAGE[0] and x > 600 and x < 950 and y > 100 and y < 200:
            self.set_intension(CATEGORIES[1])
            return
        pass

    def set_intension(self, text):
        self.intension = text
        self.stage = STAGE[2]
        deck = TarotDeck()
        deck.shuffle()
        self.drawn_cards = deck.draw(3)


def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
import arcade

# Screen title and size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "My first Game"
DEFAULT_LINE_HEIGHT = 24
DEFAULT_FONT_SIZE = 16

INTRO_TEXT = "Ah, welcome, traveler! I am Mama Nyah, and the spirits have brought you to me for a reason. Sit, relax, and let us see what the universe whispers for you. But first, tell me—what is your intention? What does your heart seek to know, heal, or discover? Speak it, and we will find the truth together."
CATEGORIES = ["Love Life", "Professional Development"]
class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.IMPERIAL_PURPLE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        pass

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()
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

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """
        pass

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """
        pass


def main():
    """ Main function """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
import arcade

DEFAULT_FONT_SIZE = 16
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
DEFAULT_LINE_HEIGHT = 24

INTRO_TEXT = (
    "Ah, welcome, traveler!\n\n"
    "I am Mama Nyah, and the spirits have brought you to me for a reason.\n\n"
    "Sit, relax, and let us see what the universe whispers for you.\n\n"
    "But first, tell me—what is your intention? What does your heart seek to know, heal, or discover?\n\n"
    "Speak it, and we will find the truth together."
)

CATEGORIES = ["Love Life", "Professional Development", "Family and Friends", "Health", "Personal Growth", "Gain Clarity"]

def outside_stage(game):
    inside_button_texture = (
                        game.button_pressed_texture if game.hovered_button == "step_inside" else game.button_texture
                    )
    exit_button_texture = (
                    game.button_pressed_texture if game.hovered_button == "exit_game" else game.button_texture
                )

    arcade.draw_texture_rectangle(
        game.x_right_button+200,
        50,
        350 //2,
        200 // 2,
        exit_button_texture)
    
    arcade.draw_text(
                "Exit",
                game.x_right_button + 75,
                45,
                arcade.color.WHITE,
                DEFAULT_FONT_SIZE,
                width=250,
                align="center",
                font_name="Old School Adventures"
            )
    
    arcade.draw_texture_rectangle(
        game.x_middle_button,
        100,
        350,
        200,
        inside_button_texture)
    
    arcade.draw_text(
                "Step Inside",
                game.x_middle_button - 125,
                95,
                arcade.color.WHITE,
                DEFAULT_FONT_SIZE,
                width=250,
                align="center",
                font_name="Old School Adventures"
            )
    
def draw_intro_stage(game):
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
                game.button_pressed_texture if game.hovered_button == f"button_{i}" else game.button_texture
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
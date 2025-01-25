import arcade

DEFAULT_FONT_SIZE = 16


class Button():
    def __init__(
            self,
            game,
            name,
            copy,
            x_center,
            y_center,
            width,
            height,
            text_x_start,
            text_y_start, 
            text_width,
        ):
        button_texture = arcade.load_texture("assets/original/Purple Button Big.png")
        button_pressed_texture = arcade.load_texture("assets/original/Purple Button Pressed Big.png")

        applied_text = button_pressed_texture if game.hovered_button == name else button_texture
        
        arcade.draw_texture_rectangle(
            x_center,
            y_center,
            width,
            height,
            applied_text
        )
        
        arcade.draw_text(
            copy,
            text_x_start,
            text_y_start,
            arcade.color.WHITE,
            DEFAULT_FONT_SIZE,
            width=text_width,
            align="center",
            font_name="Old School Adventures"
        )

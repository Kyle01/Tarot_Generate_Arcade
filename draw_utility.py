import arcade

DEFAULT_FONT_SIZE = 16

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
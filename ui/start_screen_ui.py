import arcade
from base_ui import UI

class StartScreenUi:

    def __init__(self, game)
          self.game = game
        
    def __draw_outside_stage(self):
            inside_button_texture = (
                            self.button_pressed_texture if self.hovered_button == "step_inside" else self.button_texture
                        )
            exit_button_texture = (
                            self.button_pressed_texture if self.hovered_button == "exit_game" else self.button_texture
                        )

            arcade.draw_texture_rectangle(
                self.x_right_button+200,
                50,
                350 //2,
                200 // 2,
                exit_button_texture)
            
            arcade.draw_text(
                        "Exit",
                        self.x_right_button + 75,
                        45,
                        arcade.color.WHITE,
                        DEFAULT_FONT_SIZE,
                        width=250,
                        align="center",
                        font_name="Old School Adventures"
                    )
            
            arcade.draw_texture_rectangle(
                self.x_middle_button,
                100,
                350,
                200,
                inside_button_texture)
            
            arcade.draw_text(
                        "Step Inside",
                        self.x_middle_button - 125,
                        95,
                        arcade.color.WHITE,
                        DEFAULT_FONT_SIZE,
                        width=250,
                        align="center",
                        font_name="Old School Adventures"
                    )
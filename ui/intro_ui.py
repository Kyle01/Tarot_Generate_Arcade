
    def __draw_intro_stage(self):
       
        

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


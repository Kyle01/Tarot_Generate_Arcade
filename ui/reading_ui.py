 
##try refactoring down to 200

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
        self.line_spacing= 50
        for i, line in enumerate(self.fortune[0].split('\n')):
                arcade.draw_text(
                    line,
                    SCREEN_WIDTH //2 ,
                    SCREEN_HEIGHT // 2 - (i * self.line_spacing),
                    arcade.color.WHITE,
                    font_size=18,
                    anchor_x="center",
                    anchor_y="top",
                    width=SCREEN_WIDTH * 0.8,
                    align="center",
                    font_name="Old School Adventures"
            )

        
        button_texture = (
                        self.button_pressed_texture if self.hovered_button == "next_card" else self.button_texture
                    )


        arcade.draw_texture_rectangle(
            self.x_middle_button,
            100,
            350,
            200,
            button_texture)
        
        arcade.draw_text(
                    "View Past Card",
                    self.x_middle_button - 125,
                    95,
                    arcade.color.WHITE,
                    DEFAULT_FONT_SIZE,
                    width=250,
                    align="center",
                    font_name="Old School Adventures"
                )

        for i, card in enumerate(self.drawn_cards):
            x = 350 + (i * 275)
            y = 700
            card.paint(x, y, show_front=True, scale = 2.2, is_small = True)

    def _draw_reading_card(self, card_index):
        """ Render a single card stage. """
        # Placeholder logic for displaying one card
        
        paragraph = self.fortune[card_index]
        for i, line in enumerate(paragraph.split('\n')):
            arcade.draw_text(
                line,
                SCREEN_WIDTH * .7 ,  # Left-aligned starting position
                SCREEN_HEIGHT * .75 - (i * self.line_spacing),
                arcade.color.WHITE,
                font_size=18,
                anchor_x="center",
                anchor_y="top",
                width=SCREEN_WIDTH * 0.6,  # Define width for wrapping
                align="center",
                font_name="Old School Adventures"
            )
        card = self.drawn_cards[card_index - 1]  # Cards are 0-indexed
        card.paint(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, show_front=True)

        next_button_texture = (
                        self.button_pressed_texture if self.hovered_button == "next_card" else self.button_texture
                    )
        previous_button_texture = (
                        self.button_pressed_texture if self.hovered_button == "previous_card" else self.button_texture
                    )

        previous_button_copy = None
        next_button_copy = None
        next_button_copy_y = 120
        previous_button_copy_y =95
        if card_index == 1:
            next_button_copy_y = 110
            next_button_copy = "View Present Card"
            previous_button_copy_y = 95
            previous_button_copy = "Go Back"
        elif card_index == 2:
            next_button_copy_y = 110
            next_button_copy = "View Future Card"
            previous_button_copy_y = 105
            previous_button_copy = "Return to Past Card"
        elif card_index == 3:
            next_button_copy_y = 95
            next_button_copy = "View Summary"
            previous_button_copy_y = 110
            previous_button_copy = "Return to Present Card"

        arcade.draw_texture_rectangle(
            self.x_right_button,
            100,
            350,
            200,
            previous_button_texture)
        
        arcade.draw_text(
                    next_button_copy,
                    self.x_right_button - 125,
                    next_button_copy_y,
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
            next_button_texture)
        
        arcade.draw_text(
                    previous_button_copy,
                    self.x_left_button - 125,
                    previous_button_copy_y,
                    arcade.color.WHITE,
                    DEFAULT_FONT_SIZE,
                    width=250,
                    align="center",
                    font_name="Old School Adventures"
                )

    def _draw_reading_summary(self):
        """ Render the summary stage with all cards and a summary. """
        # Placeholder logic
        
        for i, line in enumerate(self.fortune[4].split('\n')):
                arcade.draw_text(
                    line,
                    SCREEN_WIDTH //2 ,
                    SCREEN_HEIGHT // 2 +25 - (i * self.line_spacing),
                    arcade.color.WHITE,
                    font_size=18,
                    anchor_x="center",
                    anchor_y="top",
                    width=SCREEN_WIDTH * 0.8,
                    align="center",
                    font_name="Old School Adventures"
            )

        previous_button_texture = (
                        self.button_pressed_texture if self.hovered_button == "previous_card" else self.button_texture
                    )
        outside_button_texture =(self.button_pressed_texture if self.hovered_button == "go_outside" else self.button_texture
                    )
        restart_button_texture = (self.button_pressed_texture if self.hovered_button == "new_reading" else self.button_texture
                    )
        
        arcade.draw_texture_rectangle(
            self.x_middle_button,
            100,
            350,
            200,
            restart_button_texture)
        
        arcade.draw_text(
                    "New Reading",
                    self.x_middle_button - 125,
                    95,
                    arcade.color.WHITE,
                    DEFAULT_FONT_SIZE,
                    width=250,
                    align="center",
                    font_name="Old School Adventures"
                )
        
        arcade.draw_texture_rectangle(
            self.x_right_button +100,
            100,
            350,
            200,
            outside_button_texture)
        
        arcade.draw_text(
                    "Say Goodbye",
                    self.x_right_button - 25,
                    95,
                    arcade.color.WHITE,
                    DEFAULT_FONT_SIZE,
                    width=250,
                    align="center",
                    font_name="Old School Adventures"
                )
        
        arcade.draw_texture_rectangle(
            self.x_left_button-100,
            100,
            350,
            200,
            previous_button_texture)
        
        arcade.draw_text(
                    "Return to Future Card",
                    self.x_left_button - 225,
                    110,
                    arcade.color.WHITE,
                    DEFAULT_FONT_SIZE,
                    width=250,
                    align="center",
                    font_name="Old School Adventures"
                )

        for i, card in enumerate(self.drawn_cards):
            x = 350 + (i * 275)
            y = 700
            card.paint(x, y, show_front=True, scale = 2.2, is_small = True)
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
                    95,
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
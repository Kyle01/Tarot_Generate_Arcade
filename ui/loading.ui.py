 def __draw_loading_stage(self):
        """ Render the loading screen. """

        # Draw Loading Text
        arcade.draw_text(
            "Loading, please wait...",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 4,
            arcade.color.WHITE,
            DEFAULT_FONT_SIZE * 1.5,
            width=SCREEN_WIDTH,
            align="center",
            anchor_x="center",
            font_name="Old School Adventures"
        )

        # Progress bar dimensions
        bar_x = 100  # Starting x position of the bar
        bar_y = 300  # y position of the bar
        bar_height = 65  # Height of the progress bar
        cap_width = 35
        total_bar_width = 1050  # Total width of the progress bar background
        progress_width = self.loading_progress * (total_bar_width-50)  # Dynamic width of the stretchable section
        frame_width = 3296 //4
        frame_height = 68


        progress_bar_sprites = arcade.load_spritesheet(
                "assets/original/pBarBackgroundSpriteSheet.png",  # Path to the sprite sheet
                sprite_width=frame_width,  # Width of each frame
                sprite_height=frame_height,  # Height of each frame
                columns=4,  # Number of columns in the sprite sheet
                count=4  # Total number of frames
            )
        
        frame_index = int(self.frame_timer // self.frame_rate) % 4 

        # Load textures
        background_texture = arcade.load_texture("assets/original/pBarBackground.png")
        stretch_texture = arcade.load_texture("assets/original/pBarStretch.png")
        front_texture = arcade.load_texture("assets/original/pBarFront.png")
        end_texture = arcade.load_texture("assets/original/pBarEnd.png")

        arcade.draw_texture_rectangle(
            bar_x + total_bar_width // 2,  # Centered at the current progress width
            bar_y + bar_height // 2,
            total_bar_width,  # Dynamic width
            bar_height,
            progress_bar_sprites[frame_index]  # Use the correct frame
        )
        # Draw the static background
        arcade.draw_texture_rectangle(
            bar_x + total_bar_width // 2,  # Centered horizontally
            bar_y + bar_height // 2,  # Centered vertically
            total_bar_width,  # Full width
            bar_height,  # Full height
            background_texture
        )

        progress_width = self.loading_progress * (total_bar_width - 50)  # Dynamic width

        arcade.draw_texture_rectangle(
            bar_x+25,  # At the end of the progress bar
            bar_y + bar_height // 4 + 15,
            cap_width,  # Width of the front cap
            bar_height -10,
            front_texture
        )
        arcade.draw_texture_rectangle(
            bar_x + progress_width + cap_width / 2,  # Position at the end of the progress
            bar_y + bar_height // 2,
            cap_width,  # Width of the end cap
            bar_height-10,
            end_texture)

        # Draw the stretchable section of the progress bar
        current_x = bar_x  # Start position for the stretchable section
        while current_x +25 < bar_x + progress_width:  # Leave space for the front cap
            arcade.draw_texture_rectangle(
                current_x+cap_width,  # Centered segment
                bar_y + bar_height // 2,
                15,  # Width of each segment
                bar_height-10,
                stretch_texture
            )
            current_x += 10  # Move to the next segment


        # Draw Additional Text
        arcade.draw_text(
            "Please hold on while we prepare your reading...",
            SCREEN_WIDTH // 2,
            200,
            arcade.color.WHITE,
            DEFAULT_FONT_SIZE,
            width=SCREEN_WIDTH - 200,
            align="center",
            anchor_x="center",
            font_name="Old School Adventures"
        )

        # Draw the selected cards
        for i, card in enumerate(self.drawn_cards):
            x = 350 + (i * 275)  # Spaced out horizontally
            y = 575  # Fixed y-coordinate
            card.paint(x, y, show_front=True,scale=2.2, is_small=True)

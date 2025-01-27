import arcade
from button import Button

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
    Button(
        game=game,
        name='exit_game',
        copy="Exit",
        x_center=game.x_right_button+200,
        y_center=50,
        width=350 //2,
        height=200 // 2,
        text_x_start=game.x_right_button + 75,
        text_y_start=45,
    )

    Button(
        game=game,
        name='step_inside',
        copy="Step Inside",
        x_center=SCREEN_WIDTH // 2,
        y_center=100,
        text_x_start=SCREEN_WIDTH // 2 - 125,
        text_y_start=95,
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
            Button(
                game=game,
                name=f"button_{i}",
                copy=CATEGORIES[i],
                x_center=x,
                y_center=y,
                text_x_start=x-125,
                text_y_start=y,
            )

def draw_spread_stage(game):
        """ Render the card spread stage with the backs of the cards. """
        if game.reveal_active and game.current_revealed_card:
            # Draw the revealed card in the center
            game.current_revealed_card.paint(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, show_front=True, scale=1.8, is_small=False)
            button_name = "pull_next" if len(game.selected_cards) <= 2 else "begin_reading"
            button_copy = "Pull Next Card" if len(game.selected_cards) <= 2 else "Begin Reading" 

            Button(
                game=game,
                name=button_name,
                copy=button_copy,
                x_center=game.x_middle_button,
                y_center=100,
                text_x_start=game.x_middle_button - 125,
                text_y_start=95,
            )
            
            arcade.draw_text(
                f"{game.current_revealed_card.name}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 4.5,
                arcade.color.WHITE,
                DEFAULT_FONT_SIZE * 1.8,
                width=SCREEN_WIDTH,
                align="center",
                anchor_x="center",
                font_name="Old School Adventures"
            )

            if len(game.selected_cards) >1 and game.selected_cards[1]:
                x = 300 
                y = 200  
                game.selected_cards[0].paint(x, y, show_front=True, is_small=True)
            
            if len(game.selected_cards) > 2 and game.selected_cards[2]:
                x=975
                y=200
                game.selected_cards[1].paint(x,y,show_front=True, is_small = True)

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
        card_spacing = (SCREEN_WIDTH - 300) // len(game.deck.cards)  # Dynamic spacing
        for i, card in enumerate(game.deck.cards):
            x = 150 + (i * card_spacing)
            y = SCREEN_HEIGHT // 2
            card.paint(x, y, show_front=False, is_hovered=(card == game.hovered_card), is_small=True)

        # Draw previously selected cards in the left corner
        for i, card in enumerate(game.selected_cards):
            x = 300 + (i * 675)  # Spaced out horizontally with 150 pixels between cards
            y = 200  # Fixed y-coordinate for all cards
            card.paint(x, y, show_front=True, is_small=True)

def draw_loading_stage(game):
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
    progress_width = game.loading_progress * (total_bar_width-50)  # Dynamic width of the stretchable section
    frame_width = 3296 //4
    frame_height = 68


    progress_bar_sprites = arcade.load_spritesheet(
            "assets/original/pBarBackgroundSpriteSheet.png",  # Path to the sprite sheet
            sprite_width=frame_width,  # Width of each frame
            sprite_height=frame_height,  # Height of each frame
            columns=4,  # Number of columns in the sprite sheet
            count=4  # Total number of frames
        )
    
    frame_index = int(game.frame_timer // game.frame_rate) % 4 

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

    progress_width = game.loading_progress * (total_bar_width - 50)  # Dynamic width

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
    for i, card in enumerate(game.drawn_cards):
        x = 350 + (i * 275)  # Spaced out horizontally
        y = 575  # Fixed y-coordinate
        card.paint(x, y, show_front=True,scale=2.2, is_small=True)

def draw_reading_intro(game):
    """ Render the intro stage with all cards shown. """
    # Placeholder logic
    game.line_spacing= 50
    for i, line in enumerate(game.fortune[0].split('\n')):
            arcade.draw_text(
                line,
                SCREEN_WIDTH //2 ,
                SCREEN_HEIGHT // 2 - (i * game.line_spacing),
                arcade.color.WHITE,
                font_size=18,
                anchor_x="center",
                anchor_y="top",
                width=SCREEN_WIDTH * 0.8,
                align="center",
                font_name="Old School Adventures"
        )

    Button(
        game=game,
        name="next_card",
        copy="Next Card",
        x_center=game.x_middle_button,
        y_center=100,
        text_x_start=game.x_middle_button - 125,
        text_y_start=95,
    )

    for i, card in enumerate(game.drawn_cards):
        x = 350 + (i * 275)
        y = 700
        card.paint(x, y, show_front=True, scale = 2.2, is_small = True)

def draw_reading_card(game, card_index):
        """ Render a single card stage. """
       
        
        paragraph = game.fortune[card_index]
        for i, line in enumerate(paragraph.split('\n')):
            arcade.draw_text(
                line,
                SCREEN_WIDTH * .7 ,  # Left-aligned starting position
                SCREEN_HEIGHT * .75 - (i * game.line_spacing),
                arcade.color.WHITE,
                font_size=18,
                anchor_x="center",
                anchor_y="top",
                width=SCREEN_WIDTH * 0.6,  # Define width for wrapping
                align="center",
                font_name="Old School Adventures"
            )
        card = game.drawn_cards[card_index - 1]  # Cards are 0-indexed
        card.paint(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, show_front=True)

        Button(
            game=game,
            name="next_card",
            copy="Next Card",
            x_center=game.x_right_button,
            y_center=100,
            text_x_start=game.x_right_button - 125,
            text_y_start=95,
        )

        Button(
            game=game,
            name="previous_card",
            copy="Previous Card",
            x_center=game.x_left_button,
            y_center=100,
            text_x_start=game.x_left_button - 125,
            text_y_start=95,
        )

def draw_reading_summary(game):
        """ Render the summary stage with all cards and a summary. """
        # Placeholder logic
        
        for i, line in enumerate(game.fortune[4].split('\n')):
                arcade.draw_text(
                    line,
                    SCREEN_WIDTH //2 ,
                    SCREEN_HEIGHT // 2 +25 - (i * game.line_spacing),
                    arcade.color.WHITE,
                    font_size=18,
                    anchor_x="center",
                    anchor_y="top",
                    width=SCREEN_WIDTH * 0.8,
                    align="center",
                    font_name="Old School Adventures"
            )

        Button(
            game=game,
            name="new_reading",
            copy="New Reading",
            x_center=game.x_middle_button,
            y_center=100,
            text_x_start=game.x_middle_button - 125,
            text_y_start=95,
        )

        Button(
            game=game,
            name="go_outside",
            copy="Go Outside",
            x_center=game.x_right_button + 100,
            y_center=100,
            text_x_start=game.x_right_button - 25,
            text_y_start=95,
        )

        Button(
            game=game,
            name="previous_card",
            copy="Previous",
            x_center=game.x_left_button - 100,
            y_center=100,
            text_x_start=game.x_left_button - 225,
            text_y_start=95,
        )

        for i, card in enumerate(game.drawn_cards):
            x = 350 + (i * 275)
            y = 700
            card.paint(x, y, show_front=True, scale = 2.2, is_small = True)
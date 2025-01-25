import arcade
import pyglet
from game import GameState
from start_screen_ui import StartScreenUi
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
DEFAULT_LINE_HEIGHT = 24
DEFAULT_FONT_SIZE = 16
FONT_PATH = r"assets/fonts/OldSchoolAdventures-42j9.ttf"

class UI:
    def __init__(self, game):
        self.game = game
        #used only on this script
        self.background_image = arcade.load_texture("assets/original/TableClothbigger.png") 
        self.start = StartScreenUi(self)

        #used on multiple lower scripts



        #used on single lower script, move

        
        arcade.set_background_color(arcade.color.IMPERIAL_PURPLE)
        self.button_pressed_texture = arcade.load_texture("assets/original/Purple Button Pressed Big.png")
        self.button_texture = arcade.load_texture("assets/original/Purple Button Big.png")
        self.outside_image = arcade.set_background_color(arcade.color.IMPERIAL_PURPLE) ## replace with cover art
        pyglet.font.add_file(FONT_PATH)  # Load the font file
           
        self.button_clickbox_width = 175
        self.button_clickbox_height = 150
        self.x_middle_button = SCREEN_WIDTH // 2
        self.x_left_button = SCREEN_WIDTH // 4
        self.x_right_button = SCREEN_WIDTH * .75
        self.y_bottom_button = 25

    

    def draw(self, stage):
        """ Render the screen. """
        # Clear the screen
    
        self.clear()
        if stage != GameState.OUTSIDE:
            arcade.draw_lrwh_rectangle_textured(0,0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_image)
        if stage == GameState.OUTSIDE:
            arcade.set_background_color(arcade.color.IMPERIAL_PURPLE)
            # arcade.draw_lrwh_rectangle_textured(0,0, SCREEN_WIDTH, SCREEN_HEIGHT, self.outside_image)  --keep this for later
            self.start.__draw_outside_stage()
        elif stage == GameState.INTRO:
            self.__draw_intro_stage()t
        elif stage == GameState.SPREAD:
            self.__draw_spread_stage()
        elif stage == GameState.LOADING:
            self.__draw_loading_stage()
        elif stage in {
            GameState.READING_INTRO,
            GameState.READING_CARD_1,
            GameState.READING_CARD_2,
            GameState.READING_CARD_3,
            GameState.READING_SUMMARY,
        }:
            self.__draw_reading_stage()  # Centralized logic for all reading sub-stages






              '''For Debugging Hittboxes'''
        # hitbox_x = self.x_right_button + 200
        # hitbox_y = self.y_bottom_button - 50 + (self.button_clickbox_height // 4)  # Center the y-coordinate
        # hitbox_width = self.button_clickbox_width
        # hitbox_height = self.button_clickbox_height // 2

        # 
        # arcade.draw_rectangle_outline(
        #     center_x=hitbox_x,
        #     center_y=hitbox_y,
        #     width=hitbox_width,
        #     height=hitbox_height,
        #     color=arcade.color.RED,  # Red color for visibility
        #     border_width=2
        # )



   

    # def __draw_intro_stage(self):
       
        

    #     # Intro text
    #     arcade.draw_text(
    #         INTRO_TEXT,
    #         0,
    #         SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 5,
    #         arcade.color.WHITE,
    #         DEFAULT_FONT_SIZE,
    #         width=SCREEN_WIDTH,
    #         multiline=True,
    #         align="center",
    #         font_name="Old School Adventures"
    #     )

    #     # Button positions
    #     button_positions = [
    #         (275, 300),  # Button 0
    #         (650, 300),  # Button 1
    #         (1025, 300),  # Button 2
    #         (275, 150),  # Button 3
    #         (650, 150),    # Button 4
    #         (1025, 150)     # Button 5
    #     ]

    #     # Loop through categories and draw buttons
    #     for i, (x, y) in enumerate(button_positions):
    #         button_texture = (
    #             self.button_pressed_texture if self.hovered_button == f"button_{i}" else self.button_texture
    #         )
    #         arcade.draw_texture_rectangle(x, y, 350, 200, button_texture)

    #         arcade.draw_text(
    #             CATEGORIES[i],
    #             x - 125,  # Center text
    #             y,   # Position text slightly below center
    #             arcade.color.WHITE,
    #             DEFAULT_FONT_SIZE,
    #             width=250,
    #             align="center",
    #             font_name="Old School Adventures"
    #         )


    # def __draw_reading_stage(self):


    #     if self.stage == GameState.READING_INTRO:
    #         self._draw_reading_intro()  # Stage 1: Show all cards and intro

    #     elif self.stage == GameState.READING_CARD_1:
    #         self._draw_reading_card(1)  # Stage 2: Show card 1

    #     elif self.stage == GameState.READING_CARD_2:
    #         self._draw_reading_card(2)  # Stage 3: Show card 2

    #     elif self.stage == GameState.READING_CARD_3:
    #         self._draw_reading_card(3)  # Stage 4: Show card 3

    #     elif self.stage == GameState.READING_SUMMARY:
    #         self._draw_reading_summary()  # Stage 5: Show all cards and summary

    # def _draw_reading_intro(self):
    #     """ Render the intro stage with all cards shown. """
    #     # Placeholder logic
    #     self.line_spacing= 50
    #     for i, line in enumerate(self.fortune[0].split('\n')):
    #             arcade.draw_text(
    #                 line,
    #                 SCREEN_WIDTH //2 ,
    #                 SCREEN_HEIGHT // 2 - (i * self.line_spacing),
    #                 arcade.color.WHITE,
    #                 font_size=18,
    #                 anchor_x="center",
    #                 anchor_y="top",
    #                 width=SCREEN_WIDTH * 0.8,
    #                 align="center",
    #                 font_name="Old School Adventures"
    #         )

        
    #     button_texture = (
    #                     self.button_pressed_texture if self.hovered_button == "next_card" else self.button_texture
    #                 )


    #     arcade.draw_texture_rectangle(
    #         self.x_middle_button,
    #         100,
    #         350,
    #         200,
    #         button_texture)
        
    #     arcade.draw_text(
    #                 "View Past Card",
    #                 self.x_middle_button - 125,
    #                 95,
    #                 arcade.color.WHITE,
    #                 DEFAULT_FONT_SIZE,
    #                 width=250,
    #                 align="center",
    #                 font_name="Old School Adventures"
    #             )

    #     for i, card in enumerate(self.drawn_cards):
    #         x = 350 + (i * 275)
    #         y = 700
    #         card.paint(x, y, show_front=True, scale = 2.2, is_small = True)

    # def _draw_reading_card(self, card_index):
    #     """ Render a single card stage. """
    #     # Placeholder logic for displaying one card
        
    #     paragraph = self.fortune[card_index]
    #     for i, line in enumerate(paragraph.split('\n')):
    #         arcade.draw_text(
    #             line,
    #             SCREEN_WIDTH * .7 ,  # Left-aligned starting position
    #             SCREEN_HEIGHT * .75 - (i * self.line_spacing),
    #             arcade.color.WHITE,
    #             font_size=18,
    #             anchor_x="center",
    #             anchor_y="top",
    #             width=SCREEN_WIDTH * 0.6,  # Define width for wrapping
    #             align="center",
    #             font_name="Old School Adventures"
    #         )
    #     card = self.drawn_cards[card_index - 1]  # Cards are 0-indexed
    #     card.paint(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, show_front=True)

    #     next_button_texture = (
    #                     self.button_pressed_texture if self.hovered_button == "next_card" else self.button_texture
    #                 )
    #     previous_button_texture = (
    #                     self.button_pressed_texture if self.hovered_button == "previous_card" else self.button_texture
    #                 )

    #     previous_button_copy = None
    #     next_button_copy = None
    #     next_button_copy_y = 120
    #     previous_button_copy_y =95
    #     if card_index == 1:
    #         next_button_copy_y = 110
    #         next_button_copy = "View Present Card"
    #         previous_button_copy_y = 95
    #         previous_button_copy = "Go Back"
    #     elif card_index == 2:
    #         next_button_copy_y = 110
    #         next_button_copy = "View Future Card"
    #         previous_button_copy_y = 105
    #         previous_button_copy = "Return to Past Card"
    #     elif card_index == 3:
    #         next_button_copy_y = 95
    #         next_button_copy = "View Summary"
    #         previous_button_copy_y = 110
    #         previous_button_copy = "Return to Present Card"

    #     arcade.draw_texture_rectangle(
    #         self.x_right_button,
    #         100,
    #         350,
    #         200,
    #         previous_button_texture)
        
    #     arcade.draw_text(
    #                 next_button_copy,
    #                 self.x_right_button - 125,
    #                 next_button_copy_y,
    #                 arcade.color.WHITE,
    #                 DEFAULT_FONT_SIZE,
    #                 width=250,
    #                 align="center",
    #                 font_name="Old School Adventures"
    #             )
        
    #     arcade.draw_texture_rectangle(
    #         self.x_left_button,
    #         100,
    #         350,
    #         200,
    #         next_button_texture)
        
    #     arcade.draw_text(
    #                 previous_button_copy,
    #                 self.x_left_button - 125,
    #                 previous_button_copy_y,
    #                 arcade.color.WHITE,
    #                 DEFAULT_FONT_SIZE,
    #                 width=250,
    #                 align="center",
    #                 font_name="Old School Adventures"
    #             )

    # def _draw_reading_summary(self):
    #     """ Render the summary stage with all cards and a summary. """
    #     # Placeholder logic
        
    #     for i, line in enumerate(self.fortune[4].split('\n')):
    #             arcade.draw_text(
    #                 line,
    #                 SCREEN_WIDTH //2 ,
    #                 SCREEN_HEIGHT // 2 +25 - (i * self.line_spacing),
    #                 arcade.color.WHITE,
    #                 font_size=18,
    #                 anchor_x="center",
    #                 anchor_y="top",
    #                 width=SCREEN_WIDTH * 0.8,
    #                 align="center",
    #                 font_name="Old School Adventures"
    #         )

    #     previous_button_texture = (
    #                     self.button_pressed_texture if self.hovered_button == "previous_card" else self.button_texture
    #                 )
    #     outside_button_texture =(self.button_pressed_texture if self.hovered_button == "go_outside" else self.button_texture
    #                 )
    #     restart_button_texture = (self.button_pressed_texture if self.hovered_button == "new_reading" else self.button_texture
    #                 )
        
    #     arcade.draw_texture_rectangle(
    #         self.x_middle_button,
    #         100,
    #         350,
    #         200,
    #         restart_button_texture)
        
    #     arcade.draw_text(
    #                 "New Reading",
    #                 self.x_middle_button - 125,
    #                 95,
    #                 arcade.color.WHITE,
    #                 DEFAULT_FONT_SIZE,
    #                 width=250,
    #                 align="center",
    #                 font_name="Old School Adventures"
    #             )
        
    #     arcade.draw_texture_rectangle(
    #         self.x_right_button +100,
    #         100,
    #         350,
    #         200,
    #         outside_button_texture)
        
    #     arcade.draw_text(
    #                 "Say Goodbye",
    #                 self.x_right_button - 25,
    #                 95,
    #                 arcade.color.WHITE,
    #                 DEFAULT_FONT_SIZE,
    #                 width=250,
    #                 align="center",
    #                 font_name="Old School Adventures"
    #             )
        
    #     arcade.draw_texture_rectangle(
    #         self.x_left_button-100,
    #         100,
    #         350,
    #         200,
    #         previous_button_texture)
        
    #     arcade.draw_text(
    #                 "Return to Future Card",
    #                 self.x_left_button - 225,
    #                 110,
    #                 arcade.color.WHITE,
    #                 DEFAULT_FONT_SIZE,
    #                 width=250,
    #                 align="center",
    #                 font_name="Old School Adventures"
    #             )

    #     for i, card in enumerate(self.drawn_cards):
    #         x = 350 + (i * 275)
    #         y = 700
    #         card.paint(x, y, show_front=True, scale = 2.2, is_small = True)
        

    # def __draw_loading_stage(self):
    #     """ Render the loading screen. """

    #     # Draw Loading Text
    #     arcade.draw_text(
    #         "Loading, please wait...",
    #         SCREEN_WIDTH // 2,
    #         SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 4,
    #         arcade.color.WHITE,
    #         DEFAULT_FONT_SIZE * 1.5,
    #         width=SCREEN_WIDTH,
    #         align="center",
    #         anchor_x="center",
    #         font_name="Old School Adventures"
    #     )

    #     # Progress bar dimensions
    #     bar_x = 100  # Starting x position of the bar
    #     bar_y = 300  # y position of the bar
    #     bar_height = 65  # Height of the progress bar
    #     cap_width = 35
    #     total_bar_width = 1050  # Total width of the progress bar background
    #     progress_width = self.loading_progress * (total_bar_width-50)  # Dynamic width of the stretchable section
    #     frame_width = 3296 //4
    #     frame_height = 68


    #     progress_bar_sprites = arcade.load_spritesheet(
    #             "assets/original/pBarBackgroundSpriteSheet.png",  # Path to the sprite sheet
    #             sprite_width=frame_width,  # Width of each frame
    #             sprite_height=frame_height,  # Height of each frame
    #             columns=4,  # Number of columns in the sprite sheet
    #             count=4  # Total number of frames
    #         )
        
    #     frame_index = int(self.frame_timer // self.frame_rate) % 4 

    #     # Load textures
    #     background_texture = arcade.load_texture("assets/original/pBarBackground.png")
    #     stretch_texture = arcade.load_texture("assets/original/pBarStretch.png")
    #     front_texture = arcade.load_texture("assets/original/pBarFront.png")
    #     end_texture = arcade.load_texture("assets/original/pBarEnd.png")

    #     arcade.draw_texture_rectangle(
    #         bar_x + total_bar_width // 2,  # Centered at the current progress width
    #         bar_y + bar_height // 2,
    #         total_bar_width,  # Dynamic width
    #         bar_height,
    #         progress_bar_sprites[frame_index]  # Use the correct frame
    #     )
    #     # Draw the static background
    #     arcade.draw_texture_rectangle(
    #         bar_x + total_bar_width // 2,  # Centered horizontally
    #         bar_y + bar_height // 2,  # Centered vertically
    #         total_bar_width,  # Full width
    #         bar_height,  # Full height
    #         background_texture
    #     )

    #     progress_width = self.loading_progress * (total_bar_width - 50)  # Dynamic width

    #     arcade.draw_texture_rectangle(
    #         bar_x+25,  # At the end of the progress bar
    #         bar_y + bar_height // 4 + 15,
    #         cap_width,  # Width of the front cap
    #         bar_height -10,
    #         front_texture
    #     )
    #     arcade.draw_texture_rectangle(
    #         bar_x + progress_width + cap_width / 2,  # Position at the end of the progress
    #         bar_y + bar_height // 2,
    #         cap_width,  # Width of the end cap
    #         bar_height-10,
    #         end_texture)

    #     # Draw the stretchable section of the progress bar
    #     current_x = bar_x  # Start position for the stretchable section
    #     while current_x +25 < bar_x + progress_width:  # Leave space for the front cap
    #         arcade.draw_texture_rectangle(
    #             current_x+cap_width,  # Centered segment
    #             bar_y + bar_height // 2,
    #             15,  # Width of each segment
    #             bar_height-10,
    #             stretch_texture
    #         )
    #         current_x += 10  # Move to the next segment


    #     # Draw Additional Text
    #     arcade.draw_text(
    #         "Please hold on while we prepare your reading...",
    #         SCREEN_WIDTH // 2,
    #         200,
    #         arcade.color.WHITE,
    #         DEFAULT_FONT_SIZE,
    #         width=SCREEN_WIDTH - 200,
    #         align="center",
    #         anchor_x="center",
    #         font_name="Old School Adventures"
    #     )

    #     # Draw the selected cards
    #     for i, card in enumerate(self.drawn_cards):
    #         x = 350 + (i * 275)  # Spaced out horizontally
    #         y = 575  # Fixed y-coordinate
    #         card.paint(x, y, show_front=True,scale=2.2, is_small=True)


    # def __draw_spread_stage(self):
    #     """ Render the card spread stage with the backs of the cards. """
    #     if self.reveal_active and self.current_revealed_card:
    #         # Draw the revealed card in the center
    #         self.current_revealed_card.paint(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, show_front=True, scale=1.8, is_small=False)

    #         if len(self.selected_cards) <= 2:
    #                 # print(f"what is hovered: {self.hovered_button}")
                   
    #                 button_texture = (
    #                     self.button_pressed_texture if self.hovered_button == "pull_next" else self.button_texture
    #                 )
    #                 button_text = "Pull Next Card"
    #         else:
    #                 # print(f"what is hovered: {self.hovered_button}")
                    
    #                 button_texture = (
    #                     self.button_pressed_texture if self.hovered_button == "begin_reading" else self.button_texture
    #                 )
    #                 button_text = "Begin Reading"

    #         arcade.draw_texture_rectangle(self.x_middle_button, 100, 350, 200, button_texture)

    #         arcade.draw_text(
    #                 button_text,
    #                 self.x_middle_button - 125,
    #                 95,
    #                 arcade.color.WHITE,
    #                 DEFAULT_FONT_SIZE,
    #                 width=250,
    #                 align="center",
    #                 font_name="Old School Adventures"
    #             )
            
    #         arcade.draw_text(
    #             f"{self.current_revealed_card.name}",
    #             SCREEN_WIDTH // 2,
    #             SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 4.5,
    #             arcade.color.WHITE,
    #             DEFAULT_FONT_SIZE * 1.8,
    #             width=SCREEN_WIDTH,
    #             align="center",
    #             anchor_x="center",
    #             font_name="Old School Adventures"
    #         )

    #         if len(self.selected_cards) >1 and self.selected_cards[1]:

    #             x = 300 
    #             y = 200  
    #             self.selected_cards[0].paint(x, y, show_front=True, is_small=True)
            
    #         if len(self.selected_cards) > 2 and self.selected_cards[2]:

    #             x=975
    #             y=200
    #             self.selected_cards[1].paint(x,y,show_front=True, is_small = True)

    #         return  # Stop drawing the rest of the stage while reveal is active


    #     # Draw instruction text
    #     arcade.draw_text(
    #         "Choose 3 Cards:",
    #         SCREEN_WIDTH // 2,
    #         SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 4.5,
    #         arcade.color.WHITE,
    #         DEFAULT_FONT_SIZE *1.5,
    #         width=SCREEN_WIDTH,
    #         align="center",
    #         anchor_x="center",
    #         font_name="Old School Adventures"
    #     )

    #     # Draw the cards
    #     card_spacing = (SCREEN_WIDTH - 300) // len(self.deck.cards)  # Dynamic spacing
    #     for i, card in enumerate(self.deck.cards):
    #         x = 150 + (i * card_spacing)
    #         y = SCREEN_HEIGHT // 2
    #         card.paint(x, y, show_front=False, is_hovered=(card == self.hovered_card), is_small=True)

    #     # Draw previously selected cards in the left corner
    #     for i, card in enumerate(self.selected_cards):
    #         x = 300 + (i * 675)  # Spaced out horizontally with 150 pixels between cards
    #         y = 200  # Fixed y-coordinate for all cards
    #         card.paint(x, y, show_front=True, is_small=True)

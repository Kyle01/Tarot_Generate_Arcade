import arcade

import textwrap


DEFAULT_FONT_SIZE = 16
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
DEFAULT_LINE_HEIGHT = 24

def draw_outlined_text_multiline(text, x, y, font_size=DEFAULT_FONT_SIZE, font_name="Old School Adventures",
                                 color=arcade.color.WHITE, outline_color=arcade.color.BLACK,
                                 outline_thickness=2, width=SCREEN_WIDTH, line_height=DEFAULT_LINE_HEIGHT, align="center"):
    """
    Draw outlined multiline text with proper handling of `\n\n` line breaks.
    :param text: The text to be drawn (can include multiple lines and paragraphs).
    :param x: X position (center of the text block).
    :param y: Y position (top of the text block).
    :param font_size: Font size.
    :param font_name: Name of the font to use.
    :param color: The main color of the text.
    :param outline_color: The color of the outline.
    :param outline_thickness: Thickness of the outline.
    :param width: Maximum width for text wrapping.
    :param line_height: Space between lines.
    :param align: Alignment of the text ("center", "left", "right").
    """


    # Split the text into paragraphs based on `\n\n`
    paragraphs = text.split("\n\n")

    current_y = y  # Start from the top of the text block

    for paragraph in paragraphs:
        # Wrap the paragraph into lines based on the width
        lines = textwrap.wrap(paragraph, width=width // font_size)

        for line in lines:
            # Draw the outline for each line
            for dx, dy in [(-outline_thickness, 0), (outline_thickness, 0), (0, -outline_thickness), (0, outline_thickness),
                           (-outline_thickness, -outline_thickness), (-outline_thickness, outline_thickness),
                           (outline_thickness, -outline_thickness), (outline_thickness, outline_thickness)]:
                arcade.draw_text(
                    line,
                    x + dx,
                    current_y + dy,
                    outline_color,
                    font_size,
                    anchor_x=align,
                    font_name=font_name
                )

            # Draw the main text for each line
            arcade.draw_text(
                line,
                x,
                current_y,
                color,
                font_size,
                anchor_x=align,
                font_name=font_name
            )

            # Move to the next line
            current_y -= line_height

        # Add extra space between paragraphs
        current_y -= line_height * 0.5


def set_typing_text(game, new_text):
    """
    Sets the text to be typed dynamically.
    Only resets typing if the text is different.
    """
    if game.current_text != new_text:  # Only reset if the text is different
        game.current_text = new_text
        game.displayed_text = ""  # Reset displayed text
        game.text_index = 0       # Reset typing progress
        game.typing_timer = 0  


def set_paragraph_typing(game, paragraph):
    """
    Sets up the typing effect for a multi-line paragraph.
    """
    
    if not game.lines_to_type or game.current_text != paragraph:  # Prevent resetting
        game.lines_to_type = paragraph.split('\n')  # Split the paragraph into lines
        game.current_line_index = 0  
        # print(f"Lines to type{len(game.lines_to_type)}" )             # Start with the first line
        set_typing_text(game, game.lines_to_type[0])  


def update_typing_effect(game, delta_time):
    """
    Updates the typing effect, moving to the next line if necessary.
    """
    game.typing_timer += delta_time
    
    if game.typing_timer >= game.typing_speed:
        if game.text_index < len(game.current_text):  # Typing the current line
            game.text_index += 1
            game.displayed_text = game.current_text[:game.text_index]
            game.typing_timer = 0
        else:  # Current line is finished
            if game.current_line_index < len(game.lines_to_type) - 1:
                # Move to the next line
                print("Line is finished")
                game.current_line_index += 1
                print(f"current line idex= {game.current_line_index}")
                set_typing_text(game, game.lines_to_type[game.current_line_index])
            else:
                # All lines are finished
                
                game.typing_complete = True

def reset_typing_state(game):
    """
    Resets typing-related state for transitioning to a new stage or card.
    """
    game.active_card_index = None
    game.current_line_index = 0
    game.lines_to_type = []
    game.current_text = ""
    game.displayed_text = ""
    game.typing_complete = False
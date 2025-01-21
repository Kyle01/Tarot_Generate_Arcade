 
for x in [1,2,3]:
            paragraph = self.fortune[x]
            for i, line in enumerate(paragraph.split('\n')):
                arcade.draw_text(
                    line,
                    SCREEN_WIDTH * .2,
                    SCREEN_HEIGHT // 2 - 50 - (i * line_spacing),
                    arcade.color.WHITE,
                    font_size=14,
                    anchor_x="left",
                    anchor_y="top",
                    align="center",
                    font_name="Old School Adventures"
            )
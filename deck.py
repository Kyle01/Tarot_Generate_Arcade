import random
import arcade

positions = ['Upright', 'Reversed']

class Card:
    def __init__(self, name, file_name):
        self.name = name 
        self.file_name = file_name
        self.position = positions[0]

    def __str__(self):
        return f"{self.name} - {self.position}"

    def reverse(self):
        self.position = positions[1]

    def paint(self, x, y):
        texture = arcade.load_texture(f"./assets/copyright/{self.file_name}")
        if self.position == positions[0]:
            arcade.draw_scaled_texture_rectangle(x, y, texture, 1.8, 0)
        else:
            arcade.draw_scaled_texture_rectangle(x, y, texture, 1.8, 180)


class TarotDeck:
    def __init__(self):
        self.cards = [
            Card("The Fool", "major0_fool.png"),
            Card("The Magician", "major1_magician.png"),
            Card("The High Priestess", "major2_priestess.png"),
            Card("The Empress", "major3_empress.png"),
            Card("The Emperor", "major4_emperor.png"),
            Card("The Hierophant", "major5_hierophant.png"),
            Card("The Lovers", "major6_lovers.png"),
            Card("The Chariot", "major7_chariot.png"),
            Card("Strength", "major8_strength.png"),
            Card("The Hermit", "major9_hermit.png"),
            Card("Wheel of Fortune", "major10_wheel.png"),
            Card("Justice", "major11_justice.png"),
            Card("The Hanged Man", "major12_hanged.png"),
            Card("Death", "major13_death.png"),
            Card("Temperance", "major14_temperance.png"),
            Card("The Devil", "major15_devil.png"),
            Card("The Tower", "major16_tower.png"),
            Card("The Star", "major17_star.png"),
            Card("The Moon", "major18_moon.png"),
            Card("The Sun", "major18_sun.png"),
            Card("Judgement", "major20_judgement.png"),
            Card("The World", "major21_world.png"),
        ]
        self.card_back = Card("Card Back", "backing_diamond.png")
    def __str__(self):
        returned_str = ""
        for card in self.cards:
            returned_str += str(card) + "\n"
        return returned_str

    def shuffle(self):
        random.shuffle(self.cards)
        for card in self.cards:
            coin_flip = random.randrange(0, 2)
            if coin_flip == 1:
                card.reverse()

    def draw(self, num):
        return self.cards[0: num]

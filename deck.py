import random

positions = ['Upright', 'Reversed']

class Card:
    def __init__(self, name):
        self.name = name 
        self.position = positions[0]

    def __str__(self):
        return f"{self.name} - {self.position}"

    def reverse(self):
        self.position = positions[1]


class TarotDeck:
    def __init__(self):
        self.cards = [
            Card("The Fool"),
            Card("The Magician"),
            Card("The High Priestess"),
            Card("The Empress"),
            Card("The Emperor"),
            Card("The Hierophant"),
            Card("The Lovers"),
            Card("The Chariot"),
            Card("Strength"),
            Card("The Hermit"),
            Card("Wheel of Fortune"),
            Card("Justice"),
            Card("The Hanged Man"),
            Card("Death"),
            Card("Temperance"),
            Card("The Devil"),
            Card("The Tower"),
            Card("The Star"),
            Card("The Moon"),
            Card("The Sun"),
            Card("Judgement"),
            Card("The World"),
        ]

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
        

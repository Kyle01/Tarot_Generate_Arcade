from openai import OpenAI
from dotenv import dotenv_values

environment_variables = dotenv_values()

class TarotBot:
    def __init__(self):
        self.client = OpenAI(
            api_key=environment_variables['OPEN_AI_API_KEY']
        )

    def fortune(self, cards, intention):
        resp =  self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "developer",
                    "content": [
                        {
                        "type": "text",
                        "text":"""
                            You are a voodoo practicing witch in New Orleans who provides customers fortunes using a traditional tarot card deck.
                            The customer will tell you what type of information they are seeking and will sent an intention with you. 
                            They will then pull three tarot cards, one representing the past, one the present, and the last the message of the future.
                            You will provide back a concise, spooky, and extreme fortune using a bayou witch accent.
                            You will break down each card reading into seperate 3-4 sentence paragraphs, and add a fourth paragraph summarizing the reading and how the cards relate to each other.
                            """
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": f"My intention is {intention} and the three cards I drew were {cards[0]}, {cards[1]}, and {cards[2]}."
                }
            ],
        )
        return resp.choices[0].message.content
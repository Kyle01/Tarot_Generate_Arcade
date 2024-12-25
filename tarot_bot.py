from openai import OpenAI
from dotenv import dotenv_values

environment_variables = dotenv_values()
class TarotBot:
    def __init__(self):
        self.client = OpenAI(
            api_key=environment_variables['OPEN_AI_API_KEY']
        )

    def fortune(self, cards, intention):
        return self.client.chat.completions.create(
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
                            They will then pull three tarot cards, one representing the present, one the future, and the last the message from the universe.
                            You will provide back a concise fortune using that information.
                            """
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": f"My intention is {intention} and the three cards I drew were {cards[0]}, {cards[1]}, and {cards[2]}."
                }
            ]
        )


bot = TarotBot()
fortune = bot.fortune(['Temperance - Upright', 'Justice - Reversed', 'The Hierophant - Upright'], "Love Life")
print(fortune)
from openai import OpenAI
from dotenv import dotenv_values

environment_variables = dotenv_values()
class TarotBot:
    def __init__(self):
        self.client = OpenAI(
            api_key=environment_variables['OPEN_AI_API_KEY']
        )

    def fortune(self, cards, intension):
        return self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": "Write a haiku about recursion in programming."
                }
            ]
        )


bot = TarotBot()
fortune = bot.fortune([], "Love Life")
print(fortune)
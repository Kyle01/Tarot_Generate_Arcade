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
                            You will break down each card reading into seperate 3-4 sentence paragraphs, and add a final paragraph summarizing the reading and how the cards relate to each other.
                            Generate the fortune as plain paragraphs with no titles or headers, there should only be four line breaks.
                            There will be 5 Paragraphs.
                            Paragraph 1 should be a 2 sentence introduction or overview, ideally mentioning the intention.
                            Paragraph 2-4 should be the readings for each card
                            Paragraph 5 should be the summarization of the reading, and should be no more than 360 characters long"""
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": f"My intention is {intention} and the three cards I drew were {cards[0]}, {cards[1]}, and {cards[2]}."
                }
            ],
        )

        def token_usage(): 
            """Token cost calculator based on prices for 4.o mini"""
            input_rate = .15 / 1000000
            cached_input_rate = .075 / 1000000
            output_rate = .6 / 1000000

            cached_input_cost = resp.usage.prompt_tokens_details.cached_tokens * cached_input_rate
            input_cost = (resp.usage.prompt_tokens - resp.usage.prompt_tokens_details.cached_tokens) * input_rate
            output_cost = resp.usage.completion_tokens * output_rate
            total_cost = cached_input_cost + input_cost + output_cost

            print("\nToken Usage:")
            print(f"Prompt tokens: {resp.usage.prompt_tokens}")
            print(f"Cached Prompt tokens: {resp.usage.prompt_tokens_details.cached_tokens}")
            print(f"Completion tokens: {resp.usage.completion_tokens}")
            print(f"Total tokens: {resp.usage.total_tokens}")
            print("\n Token Cost:")
            print(f"Prompt tokens: {input_cost}")
            print(f"Cached Prompt tokens: {cached_input_cost}")
            print(f"Completion tokens: {output_cost}")
            print(f"Total tokens: {total_cost}")

        
        

    ## 

        token_usage()
        return resp.choices[0].message.content
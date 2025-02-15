from dotenv import dotenv_values
from text_utility import wrap_text_paragraphs
import requests
import os
import hashlib

def generate_auth_headers():
    """
    Generates Token and Hash headers for secure API request.
    """
    token = "player_access"  # Could be any static string or randomized per request
    secret_hash = os.getenv('SECRET_HASH')  # You can store this locally in the game too

    hasher = hashlib.sha256()
    hasher.update(f"{token}{secret_hash}".encode('utf-8'))
    request_hash = hasher.hexdigest()

    return {
        "Token": token,
        "Hash": request_hash,
        "Content-Type": "application/json"
}
    
def get_fortune(game, cards, intention):
    """Send cards and intention to the Flask server to get a fortune"""
    headers = generate_auth_headers()
    card_names = [card.name for card in cards]
    try:
        response = requests.post(
            f"{game.request_url}fortune",
            headers=headers,
            json={"cards": card_names, "intention": intention}
        )

        if response.status_code == 200:
            data = response.json()
            game.fortune = data['fortune']

            # # Optional: If you want to display token usage in the console
            print(f"Tokens Used: {data['tokens_used']}")

        else:
            # Handle the error if the server returns an error response
            game.fortune = f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        # Handle network errors or other unexpected exceptions
        game.fortune = f"API Call Failed: {str(e)}"

        print(game.fortune)

    # Let the game know the API call is done, even if it failed
    game.api_call_complete = True

    # Wrap paragraphs if a valid fortune is returned
    game.fortune = wrap_text_paragraphs(game.fortune)



# this is the the cron lambda job in AWS
import hashlib
import os
import requests

def lambda_handler(event, context):
    URL = 'https://tarot-generate-arcade.onrender.com/reset_tokens'
    secret = os.environ['secret']
    random_bytes = os.urandom(32)
    hashed_token = hashlib.sha256(random_bytes).hexdigest()
    
    hasher = hashlib.sha256()
    hasher.update(f'{hashed_token}{secret}'.encode('utf-8'))
    secret_hash = hasher.hexdigest()
    
    headers = { "Token": str(hashed_token), "Hash": str(secret_hash) }
    
    response = requests.get(URL, headers=headers)

    return {
        'statusCode': response.status_code,
        'body': response.content
    }


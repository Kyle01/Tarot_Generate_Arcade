import os
from flask import Flask, jsonify, request, json, abort, request
import hashlib
import psycopg2
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv() 

def verify_authentication():
    mode = os.environ.get('DEPLOY_MODE')

    if mode == 'dev':
        return True
    
    try: 
        secret = os.environ.get('SECRET_HASH')

        request_token = request.headers['Token']
        request_hash =  request.headers['Hash']

        hasher = hashlib.sha256()
        hasher.update(f'{request_token}{secret}'.encode('utf-8'))
        secret_hash = hasher.hexdigest()


        if secret_hash != request_hash:
            abort(403)
        else:
            return True
    except: 
        abort(403)

def get_db_connection():
    DB_CONNECTION_URL = os.environ.get('DB_CONNECTION_URL')
    conn = psycopg2.connect(DB_CONNECTION_URL)
    return conn

@app.route('/fortune')
def fortune():
    verify_authentication()
    return "This will be your fortune", 200

@app.route('/reset_tokens')
def reset_tokens():
    verify_authentication()
    # conn = get_db_connection()
    # cur = conn.cursor()
    # query = """
    #     SELECT *
    #     FROM song_rankings
    #     WHERE date::date = %s;

    # """
    # cur.execute(query, (formatted_date,))
    return "This endpoint will reset the monthly token count", 200
    
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
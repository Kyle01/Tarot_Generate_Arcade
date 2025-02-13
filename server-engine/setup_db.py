import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables (e.g., DB connection URL)
load_dotenv()

DB_CONNECTION_URL = os.environ.get('DB_CONNECTION_URL')

# Connect to the database
conn = psycopg2.connect(DB_CONNECTION_URL)
cur = conn.cursor()

# Optional: Drop the tables if you want a fresh start every time (useful for development)
cur.execute('DROP TABLE IF EXISTS token_tracking;')
cur.execute('DROP TABLE IF EXISTS user_requests;')

# Create token_tracking table
cur.execute('''
    CREATE TABLE token_tracking (
        id SERIAL PRIMARY KEY,
        request_count INTEGER DEFAULT 0,
        total_cost NUMERIC(10, 6) DEFAULT 0.0
    );
''')

# Create user_requests table
cur.execute('''
    CREATE TABLE user_requests (
        id SERIAL PRIMARY KEY,
        ip_address VARCHAR(45),
        user_agent TEXT,
        request_path VARCHAR(255),
        request_method VARCHAR(10),
        request_payload JSONB,
        tokens_used INTEGER,
        request_cost NUMERIC(10, 6),
        request_time TIMESTAMP DEFAULT NOW()
    );
''')

# Insert initial row for token_tracking table
cur.execute('INSERT INTO token_tracking (request_count, total_cost) VALUES (0, 0.0);')

# Commit changes and close connection
conn.commit()
cur.close()
conn.close()

print("✅ token_tracking and user_requests tables created successfully.")

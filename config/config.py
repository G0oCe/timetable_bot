import os
from dotenv import load_dotenv
import mysql.connector
import telebot as tb

load_dotenv()

def get_db_connection() -> mysql.connector.connect:
    """Establish and return a database connection."""
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
def get_bot_connection() -> tb.TeleBot:
    token = os.getenv('TOKEN')
    if not token:
        raise ValueError("Bot token is not set in environment variables.")
    return tb.TeleBot(token)

url = os.getenv('TT_URL')  # Update with the actual URL
username = os.getenv('TT_USER')  # Fetch username from environment variables
password = os.getenv('TT_PASSWORD')  # Fetch password from environment variables
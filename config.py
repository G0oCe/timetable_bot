import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

def get_db_connection() -> mysql.connector.connect:
    """Establish and return a database connection."""
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

# Example of how to get the bot token if needed
TOKEN = os.getenv('TOKEN')

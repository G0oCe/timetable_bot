import json
from config import get_db_connection

# Load faculty IDs from JSON
faculty_ids = json.load(open('faculty_ids.json', 'r', encoding='utf-8'))

def execute_query(query: str, params: tuple = ()) -> None:
    """Execute a database query."""
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute(query, params)
        db.commit()
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()
        db.close()

def insert_user(user_id: int) -> None:
    """Insert a new user into the user_table."""
    execute_query("INSERT INTO user_table (user_id) VALUES (%s);", (user_id,))

def delete_user(user_id: int) -> None:
    """Delete a user from the user_table."""
    execute_query("DELETE FROM user_table WHERE user_id=%s;", (user_id,))

def get_user(user_id: int) -> list:
    """Retrieve user information from user_table."""
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM user_table WHERE user_id=%s;", (user_id,))
    res = cursor.fetchall()
    cursor.close()
    db.close()
    return res

def get_user_subscriptions(user_id: int) -> list:
    """Get user subscriptions from the database."""
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT subscriptions FROM user_table WHERE user_id=%s;", (user_id,))
    res = cursor.fetchall()
    cursor.close()
    db.close()
    return res

def add_subscription(user_id: int, faculty: str) -> None:
    """Add a faculty subscription for a user."""
    subscriptions = get_user_subscriptions(user_id)[0][0]  # Assuming single subscription string
    new_subscriptions = f"{subscriptions};{faculty}" if subscriptions else faculty
    execute_query("UPDATE user_table SET subscriptions=%s WHERE user_id=%s;", (new_subscriptions, user_id))

def remove_subscription(user_id: int, faculty: str) -> None:
    """Remove a faculty subscription for a user."""
    subscriptions = get_user_subscriptions(user_id)[0][0]
    if subscriptions:
        subscription_list = subscriptions.split(';')
        subscription_list.remove(faculty)
        new_subscriptions = ';'.join(subscription_list)
        execute_query("UPDATE user_table SET subscriptions=%s WHERE user_id=%s;", (new_subscriptions, user_id))

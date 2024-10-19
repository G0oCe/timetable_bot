from handlers import bot  # Import the bot and handlers from handlers.py

def botStart() -> None:
    """Start polling for updates."""
    bot.polling(none_stop=True)

if __name__ == '__main__':
    botStart()

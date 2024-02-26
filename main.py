import subprocess
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, Updater


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)



# Telegram bot token
TOKEN = '6882083004:AAFBifAGRn_RnV1lljyDpj7MWSvHlB3MZjg'

# Define the command handler for the /run command
def run_script(update, context):
    # Run your Python script
    subprocess.run(["python", "tmp.py"])

    # After the script is executed, send the screenshot
    if context.bot is not None:
        context.bot.send_photo(update.message.chat_id, open('screenshot.png', 'rb'))
    else:
        logging.error("Bot object is None")

# Set up the Telegram bot



if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', run_script)
    application.add_handler(start_handler)
    
    application.run_polling()

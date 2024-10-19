import os
import json
import telebot as tb
from telebot import types
from db import insert_user, delete_user, get_user
from markup import main_menu_markup, faculties_menu_markup, course_menu_markup

# Initialize the bot using the token from environment variables
bot = tb.TeleBot(os.getenv('TOKEN'))

# Handler for the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message) -> None:
    """Send a welcome message and show the main menu."""
    insert_user(message.chat.id)  # Optionally insert the user into the database
    bot.send_message(chat_id=message.chat.id, 
                     text="Добро пожаловать! Выберите действие:",
                     reply_markup=main_menu_markup())  # Display main menu options

# Handler for the /help command
@bot.message_handler(commands=['help'])
def help_command(message: types.Message) -> None:
    """Provide help information."""
    bot.send_message(message.chat.id, "Доступные команды: /start, /help, /schedule")  # Display available commands

# Handler for the /schedule command
@bot.message_handler(commands=['schedule'])
def schedule(message: types.Message) -> None:
    """Show available schedules."""
    try:
        with open("schedule.json", "r", encoding='utf-8') as file:
            data = json.load(file)  # Load the schedule data from the JSON file
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Ошибка: Расписание не найдено.")  # Notify if the schedule file is missing
        return
    except json.JSONDecodeError:
        bot.send_message(message.chat.id, "Ошибка: Невозможно прочитать расписание.")  # Handle JSON parsing errors
        return

    # Create an inline keyboard with faculty options
    markup = types.InlineKeyboardMarkup()
    for faculty in data:
        markup.add(types.InlineKeyboardButton(faculty, callback_data=faculty))  # Add each faculty as a button
    bot.send_message(message.chat.id, text='Выберите ваш факультет: ', reply_markup=markup)  # Prompt user to select faculty

# Callback query handler for handling inline button clicks
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call: types.CallbackQuery) -> None:
    """Handle inline keyboard button queries."""
    
    # Show faculties menu when "menu_faculties" is selected
    if call.data == "menu_faculties":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Выберите факультет:",
                              message_id=call.message.message_id,
                              reply_markup=faculties_menu_markup())  # Display faculty menu
    
    # Faculty is selected, prompt the user to choose a course
    elif call.data.startswith("faculty_"):
        faculty = call.data.split("_")[1]  # Extract selected faculty
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text=f"Вы выбрали {faculty}. Теперь выберите курс:",
                              message_id=call.message.message_id,
                              reply_markup=course_menu_markup(faculty))  # Display course selection for the chosen faculty

    # Return to the course menu for the selected faculty
    elif call.data.startswith("back_to_courses_"):
        faculty = call.data.split("_")[2]  # Extract faculty name
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text=f"Выберите курс для предмета {faculty}:",
                              message_id=call.message.message_id,
                              reply_markup=course_menu_markup(faculty))  # Display course options for the faculty

    # Go back to the faculties menu
    elif call.data == "back_to_faculties":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Выберите предмет:",
                              message_id=call.message.message_id,
                              reply_markup=faculties_menu_markup())  # Go back to faculty selection

    # Return to the main menu
    elif call.data == "back_to_main_menu":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Добро пожаловать! Выберите действие:",
                              message_id=call.message.message_id,
                              reply_markup=main_menu_markup())  # Show main menu again
    
    # Show informational section if selected
    elif call.data == "menu_info":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Это информационный раздел. Вы можете вернуться в главное меню.",
                              message_id=call.message.message_id,
                              reply_markup=types.InlineKeyboardMarkup().add(
                                  types.InlineKeyboardButton(text="⬅ Назад в главное меню", callback_data="back_to_main_menu")
                              ))  # Provide an option to return to the main menu



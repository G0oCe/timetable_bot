import telebot as tb
import json
from telebot import types
import mysql.connector
from markup import main_menu_markup, faculties_menu_markup, course_menu_markup 
from dotenv import load_dotenv
import os
load_dotenv()

bot = tb.TeleBot(os.getenv('TOKEN'))

mydb = mysql.connector.connect(
  host = os.getenv('DB_HOST'),
  user = os.getenv('DB_USER'),
  password= os.getenv('DB_PASSWORD'),
  database= os.getenv('DB_NAME')
)

faculty_ids = json.load(open('faculty_ids.json', 'r', encoding='utf-8'))

mycursor = mydb.cursor()

def insert_user(id):
    mydb.commit()

def delete_user(id):
    mycursor.execute(f"DELETE FROM user_table where user_id={id};")
    mydb.commit()

def get_user(id):
    mycursor.execute(f"select * from user_table where user_id={id};")
    res = mycursor.fetchall()
    return res

def get_user_subscriptions(id):
    mycursor.execute(f"select subscriptions from user_table where user_id={id};")
    res = mycursor.fetchall()
    return res

def add_subscription(id, faculty):
    res = get_user_subscriptions(id)
    res = res + ';' + faculty
    mycursor.execute(f"update user_table SET subscriptions='{res}' where user_id={id};")
    mydb.commit()

def remove_subscription(id, faculty):
    res = get_user_subscriptions(id)
    subscriptions = res.split(';')
    subscriptions.remove(faculty)
    string = ''
    for sub in subscriptions:
        string += sub
    mycursor.execute(f"update user_table SET subscriptions='{string}' where user_id={id};")
    mydb.commit()



@bot.message_handler(commands=['start'])  # хз как это в другой файл запихать
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id, 
                     text="Добро пожаловать! Выберите действие:",
                     reply_markup=main_menu_markup())     



@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, message)

@bot.message_handler(commands=['schedule'])
def schedule(message):
    with open("schedule.json", "r", encoding='utf-8') as file:
        data = json.load(file)
    markup = types.InlineKeyboardMarkup()
    for faculty in data:
        markup.add(types.InlineKeyboardButton(faculty, callback_data="asd"))
    # schedule = data['Физика, 3 курс']
    # print(schedule)
    bot.send_message(message.chat.id, text='Выберите ваш факультет: ', reply_markup=markup)
    # bot.send_message(message.chat.id, json.dumps(schedule, indent=4, ensure_ascii=False), reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    # Главное меню -> Меню факультетов
    if call.data == "menu_faculties":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Выберите факультет:",
                              message_id=call.message.message_id,
                              reply_markup=faculties_menu_markup())
    
    # Выбор факультета -> Меню курсов
    elif call.data.startswith("faculty_"):
        faculty = call.data.split("_")[1]  # Получаем выбранный предмет
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text=f"Вы выбрали {faculty}. Теперь выберите курс:",
                              message_id=call.message.message_id,
                              reply_markup=course_menu_markup(faculty))
    

    # Возврат к меню курсов для конкретного факультета
    elif call.data.startswith("back_to_courses_"):
        faculty = call.data.split("_")[2]  # Получаем факультет
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text=f"Выберите курс для предмета {faculty}:",
                              message_id=call.message.message_id,
                              reply_markup=course_menu_markup(faculty))

    # Возврат к меню предметов
    elif call.data == "back_to_faculties":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Выберите предмет:",
                              message_id=call.message.message_id,
                              reply_markup=faculties_menu_markup())

    # Возврат в главное меню
    elif call.data == "back_to_main_menu":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Добро пожаловать! Выберите действие:",
                              message_id=call.message.message_id,
                              reply_markup=main_menu_markup())
    
    # Если выбрали "Информация" в главном меню
    elif call.data == "menu_info":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="Это информационный раздел. Вы можете вернуться в главное меню.",
                              message_id=call.message.message_id,
                              reply_markup=types.InlineKeyboardMarkup().add(
                                  types.InlineKeyboardButton(text="⬅ Назад в главное меню", callback_data="back_to_main_menu")
                              ))

@bot.message_handler()
def main(message):
    txt = message.text.lower()


def botStart():
    bot.polling(none_stop=True)

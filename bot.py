import telebot as tb
import json
from telebot import types
import mysql.connector

bot = tb.TeleBot('6827462185:AAFx3zS0E2dAbJj-UKqK9bxr9heCt-_rzZw')

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Gago6177hpmp",
  database="timetable"
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



def generate_subscribtion_markup():
    data = {}
    for faculty in list(faculty_ids.keys()):
        data[faculty] = {'callback_data': 'dsadsa'}
    markup = tb.util.quick_markup(data, row_width=2)
        # for i in range(1,5):
            # markup too long. Сделать так, чтобы сначала выбирался факультет, потом курс
            # markup.add(types.InlineKeyboardButton(f'{faculty}, {i} курс', callback_data=f'subscribe:{faculty_ids[faculty]}-{i}'))
            # Каждая кнопка должна показывать подписан или нет и подписывать или отписывать
            # Сделать кнопки динамичными и в два ряда как в https://stackoverflow.com/questions/45558984/how-to-make-telegram-bot-dynamic-keyboardbutton-in-python-every-button-on-one-ro
    return markup



@bot.message_handler(commands=['start'])
def start(message):
    try:
        insert_user(message.chat.id)
        bot.send_message(message.chat.id, 'Вы успешно зарегистрировались', parse_mode='html')
    except mysql.connector.Error as err:
        if(err.errno == 1062):
            bot.send_message(message.chat.id, 'Вы уже зарегистрированы', parse_mode='html')
        else:
            bot.send_message(message.chat.id, 'Произошла ошибка', parse_mode='html')
        


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

@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    markup = generate_subscribtion_markup()
    bot.send_message(message.chat.id, text='Выберите ваш факультет: ', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.split(":")[0]=='subscribe')
def callback_query(call):
    id = call.data.split(":")[1]
    print(call.data)

    bot.send_message(call.message.chat.id, text=f'Вы успешно подписались на {id}')
    # Добавить логику подписывания и отписывания



@bot.message_handler()
def main(message):
    txt = message.text.lower()


def botStart():
    bot.polling(none_stop=True)

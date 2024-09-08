import telebot
from telebot import types




def main_menu_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Регистрация", callback_data="menu_faculties"))
    markup.add(types.InlineKeyboardButton(text="Информация", callback_data="menu_info"))
    return markup


def faculties_menu_markup():
    markup = types.InlineKeyboardMarkup()
    faculties = ["Физика", "Химия", "Математика", "Филология", "Юриспруденция"]
    for faculty in faculties:
        markup.add(types.InlineKeyboardButton(text=faculty, callback_data=f"faculty_{faculty}"))
   
    markup.add(types.InlineKeyboardButton(text="⬅ Назад в главное меню", callback_data="back_to_main_menu"))
    return markup


def course_menu_markup(faculty):
    markup = types.InlineKeyboardMarkup()
    for course in range(1, 5):
        markup.add(types.InlineKeyboardButton(text=f"{course} курс", callback_data=f"course_{course}_{faculty}"))

    markup.add(types.InlineKeyboardButton(text="⬅ Назад к факультетам", callback_data="back_to_faculties"))
    return markup







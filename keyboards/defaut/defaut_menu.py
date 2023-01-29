from aiogram import types
import sqlite3

shop_menu_btn = [
    '🛒 Каталог',
    '💼 Мой Профиль',
    '📁 Информация',
]


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        shop_menu_btn[0],
        shop_menu_btn[1],
        shop_menu_btn[2],
    )

    conn = sqlite3.connect('./data/database.db')
    cursor = conn.cursor()

    base = cursor.execute(f'SELECT * FROM buttons').fetchall()
    x1 = 0
    x2 = 1
    try:
        for i in range(len(base)):
            markup.add(base[x1][0], base[x2][0])
            x1 += 2
            x2 += 2
    except:
        try:
            markup.add(base[x1][0])
        except:
            return markup

    return markup


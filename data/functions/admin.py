import sqlite3
from aiogram import types
from aiosqlite import connect
import random
import datetime

from utils.proxyline import ProxyLine
from utils.cheating_api import SMMPanelAPI
from data.functions.system import System


async def admin_stats():
    async with connect('./data/database.db') as db:
        select = await db.execute('SELECT * FROM users')
        row = await select.fetchall()

        d = datetime.timedelta(days=1)
        h = datetime.timedelta(hours=1)
        date = datetime.datetime.now()

        amount_user_all = 0
        amount_user_day = 0
        amount_user_hour = 0

        for i in row:
            amount_user_all += 1

            if date - datetime.datetime.fromisoformat(i[6]) <= d:
                amount_user_day += 1
            if date - datetime.datetime.fromisoformat(i[6]) <= h:
                amount_user_hour += 1

        select = await db.execute('SELECT * FROM deposit_logs')
        pay = await select.fetchall()

        qiwi = 0
        all_qiwi = 0
        banker = 0
        all_banker = 0
        chatex = 0
        all_chatex = 0
        for i in pay:
            if i[1] == 'qiwi':
                if date - datetime.datetime.fromisoformat(i[3]) <= d:
                    qiwi += i[2]

                all_qiwi += i[2]

            elif i[1] == 'banker':
                if date - datetime.datetime.fromisoformat(i[3]) <= d:
                    banker += i[2]

                all_banker += i[2]
            elif i[1] == 'chatex':
                if date - datetime.datetime.fromisoformat(i[3]) <= d:
                    chatex += i[2]

                all_chatex += i[2]

        select = await db.execute('SELECT * FROM purchase_history')
        row = await select.fetchall()

        all_purchases = 0
        day_purchases = 0
        hour_purchases = 0

        for i in row:
            if date - datetime.datetime.fromisoformat(i[5]) <= d:
                day_purchases += 1
            elif date - datetime.datetime.fromisoformat(i[5]) <= h:
                hour_purchases += 1
            all_purchases += 1

    msg = f"""
<b>💈 Информация о пользователях:</b>

❕ За все время: <b>{amount_user_all}</b>
❕ За день: <b>{amount_user_day}</b>
❕ За час: <b>{amount_user_hour}</b>

<b>💈 Пополнений за 24 часа</b>
❕ QIWI: <b>{qiwi} ₽</b>
❕ Banker: <b>{banker} ₽</b>
❕ Chatex: <b>{chatex} ₽</b>

<b>💈 Информация о продажах</b>
❕ За все время: <b>{all_purchases}</b>
❕ За день: <b>{day_purchases}</b>
❕ За час: <b>{hour_purchases}</b>

<b>💈 Ниже приведены данные за все время</b>
💳 Пополнения QIWI: <b>{all_qiwi} ₽</b>
💳 Пополнения BANKER: <b>{all_banker} ₽</b>
💳 Пополнения Chatex: <b>{all_chatex} ₽</b>
{System().info_msg()}
"""

    return msg

async def proxy_stats():
    async with connect('./data/database.db') as db:
        select = await db.execute('SELECT * FROM proxy_logs')
        row = await select.fetchall()

        d = datetime.timedelta(days=1)
        h = datetime.timedelta(hours=1)
        day7 = datetime.timedelta(days=7)
        month = datetime.timedelta(weeks=1)
        day90 = datetime.timedelta(weeks=3)
        date = datetime.datetime.now()

        all_proxy = 0
        day_proxy = 0
        hour_proxy = 0

        spending_all = 0
        spending_90d = 0 
        spending_month = 0
        spending_7d = 0
        spending_day = 0
        spending_hour = 0

        profit_all = 0
        profit_90d = 0
        profit_month = 0
        profit_7d = 0
        profit_day = 0
        profit_hour = 0

        for i in row:
            all_proxy += 1
            spending_all += float(i[15])
            profit_all += float(i[15]) - float(i[14])

            if date - datetime.datetime.fromisoformat(i[11]) <= day90:
                spending_90d += float(i[15])
                profit_90d += float(i[15]) - float(i[14])
            if date - datetime.datetime.fromisoformat(i[11]) <= month:
                spending_month += float(i[15])
                profit_month += float(i[15]) - float(i[14])
            if date - datetime.datetime.fromisoformat(i[11]) <= day7:
                spending_7d += float(i[15])
                profit_7d += float(i[15]) - float(i[14])
            if date - datetime.datetime.fromisoformat(i[11]) <= d:
                day_proxy += 1
                spending_day += float(i[15])
                profit_day += float(i[15]) - float(i[14])
            if date - datetime.datetime.fromisoformat(i[11]) <= h:
                hour_proxy += 1
                spending_hour += float(i[15])
                profit_hour += float(i[15]) - float(i[14])

    msg = f"""
<b>💈 Информация о прокси:</b>

🌀 Продано за все время: <b>{all_proxy}</b>
🌀 Продано за день: <b>{day_proxy}</b>
🌀 Продано за час: <b>{hour_proxy}</b>

🚸Пользователи потратили за все время: {round(spending_all)} ₽
🧬 Маржа за все время: {round(profit_all)} ₽

🚸 Пользователи потратили за 90 дней: {round(spending_90d)} ₽
🧬 Маржа за 90 дней: {round(profit_90d)} ₽

🚸 Пользователи потратили за 30 дней: {round(spending_month)} ₽
🧬 Маржа за 30 дней: {round(profit_month)} ₽

🚸 Пользователи потратили за 7 дней: {spending_7d} ₽
🧬 Маржа за 7 дней: {round(profit_7d)} ₽

🚸 Пользователи потратили за сутки: {spending_day} ₽
🧬 Маржа за сутки: {round(profit_day)} ₽

🚸 Пользователи потратили за час: {spending_hour} ₽
🧬 Маржа за час: {round(profit_hour)} ₽
    """
    
    return msg

async def cheating_stats():
    async with connect('./data/database.db') as db:
        select = await db.execute('SELECT * FROM cheat_logs')
        row = await select.fetchall()

        day = datetime.timedelta(days=1)
        hour = datetime.timedelta(hours=1)
        day7 = datetime.timedelta(days=7)
        month = datetime.timedelta(weeks=1)
        day90 = datetime.timedelta(weeks=3)
        date = datetime.datetime.now()

        all_cheating = 0
        day_cheating = 0
        hour_cheating = 0

        spending_all = 0
        spending_90d = 0 
        spending_month = 0
        spending_7d = 0
        spending_day = 0
        spending_hour = 0

        profit_all = 0
        profit_90d = 0
        profit_month = 0
        profit_7d = 0
        profit_day = 0
        profit_hour = 0

        for i in row:
            all_cheating += 1
            spending_all += float(i[9])
            profit_all += float(i[9]) - float(i[8])

            if date - datetime.datetime.fromisoformat(i[11]) <= day90:
                spending_90d += float(i[9])
                profit_90d += float(i[9]) - float(i[8])
            if date - datetime.datetime.fromisoformat(i[11]) <= month:
                spending_month += float(i[9])
                profit_month += float(i[9]) - float(i[8])
            if date - datetime.datetime.fromisoformat(i[11]) <= day7:
                spending_7d += float(i[9])
                profit_7d += float(i[9]) - float(i[8])
            if date - datetime.datetime.fromisoformat(i[11]) <= day:
                day_cheating += 1
                spending_day += float(i[9])
                profit_day += float(i[9]) - float(i[8])
            if date - datetime.datetime.fromisoformat(i[11]) <= hour:
                hour_cheating += 1
                spending_hour += float(i[9])
                profit_hour += float(i[9]) - float(i[8])

    msg = f"""
<b>💈 Информация о накрутке:</b>

🌀 Продано за все время: <b>{all_cheating}</b>
🌀 Продано за день: <b>{day_cheating}</b>
🌀 Продано за час: <b>{hour_cheating}</b>

🚸Пользователи потратили за все время: {spending_all} ₽
🧬 Маржа за все время: {profit_all} ₽

🚸 Пользователи потратили за 90 дней: {spending_90d} ₽
🧬 Маржа за 90 дней: {profit_90d} ₽

🚸 Пользователи потратили за 30 дней: {spending_month} ₽
🧬 Маржа за 30 дней: {profit_month} ₽

🚸 Пользователи потратили за 7 дней: {spending_7d} ₽
🧬 Маржа за 7 дней: {profit_7d} ₽

🚸 Пользователи потратили за сутки: {spending_day} ₽
🧬 Маржа за сутки: {profit_day} ₽

🚸 Пользователи потратили за час: {spending_hour} ₽
🧬 Маржа за час: {profit_hour} ₽
    """
    
    return msg

async def get_users():
    async with connect('./data/database.db') as db:
        select = await db.execute('SELECT * FROM users')
        users = await select.fetchall()

    return list(users)

class AdmPromo():
    def __init__(self) -> None:
        self.sql_path = "./data/database.db"

    async def add_promo(self, name, money, amount):
        async with connect(self.sql_path) as db:
            promo = [random.randint(111, 999), name, amount, money, "0,"]
            await db.execute(f'INSERT INTO promocode VALUES (?,?,?,?,?)', promo)
            await db.commit()

    async def activ_promo_menu(self):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM promocode')
            info = await select.fetchall()
            markup = types.InlineKeyboardMarkup()
        for i in info:
                markup.add(types.InlineKeyboardButton(text=f'🎁 {i[1]}| Kol: {i[3]} | {i[2]} ₽',callback_data=f'adm_promo:{i[0]}'))

        return markup

    async def get_info_promo(self, promo_id):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM promocode WHERE id = ?', [promo_id])
            info = await select.fetchone()
    
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add( 
                types.InlineKeyboardButton(text='Удалить', callback_data=f'promo_delete:{promo_id}'),
                types.InlineKeyboardButton(text='Выйти', callback_data='to_close'),
            )

        msg = f"""
<b>🕹 ID PROMO:</b> {info[0]}

<b>🕹 Название:</b> {info[1]}

<b>🔗 Активаций:</b> {info[3]}

<b>💰 Награда:</b> {info[2]} RUB

        """

        return msg, markup

    async def delete_promocode(self, promo_id):
        async with connect(self.sql_path) as db:
            await db.execute('DELETE FROM promocode WHERE id = ?', [promo_id])
            await db.commit()

class SendingMail():
    def __init__(self) -> None:
        self.sql_path = './data/database.db'

    async def down_sending(self, types, text, photo, date):
        async with connect(self.sql_path) as db:
            data = [types, text, photo, date]
            await db.execute('INSERT INTO sending VALUES (?,?,?,?)', data)
            await db.commit()

    async def sending_check(self):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM sending')
            row = await select.fetchall()

            for i in row:
                if datetime.datetime.fromisoformat(i[3]) <= datetime.datetime.now():
                    await db.execute('DELETE FROM sending WHERE photo = ?', [i[2]])
                    await db.commit()

                    return i
        
        return False
    
    async def down_sending_markup(self):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM sending')
            info = await select.fetchall()

        info = list(info)

        if len(info) > 0:
            markup = types.InlineKeyboardMarkup(row_width=2)
            x1 = 0
            x2 = 1
            for i in range(len(info)):
                try:
                    markup.add(
                        types.InlineKeyboardButton(text=f'💈 {info[x1][3]} 📝{info[x1][1]}', callback_data=f'info_sending:{info[x1][2]}'),
                        types.InlineKeyboardButton(text=f'💈 {info[x2][3]} 📝{info[x2][1]}', callback_data=f'info_sending:{info[x2][2]}')
                    )
                    x1 += 1
                    x2 += 1
                except:
                    try:
                        markup.add(
                            types.InlineKeyboardButton(text=f'💈 {info[x1][3]} 📝{info[x1][1]}', callback_data=f'info_sending:{info[x1][2]}')
                        )
                    except:
                        return markup

            return markup
        else:
            return False

    async def down_sending_info(self, code):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM sending WHERE photo = ?', [code])
            info = await select.fetchone()

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add( 
            types.InlineKeyboardButton(text=f'Удалить', callback_data=f'del_sending:{code}'),
            types.InlineKeyboardButton(text=f'Выйти', callback_data=f'to_closed'),
        )

        msg = f"""
<b>🖲 Тип рассылки:</b> {info[0]}
<b>🗒 Текст:</b>
{info[1]}
<b>📆 Дата:</b> {info[3]}
        """

        return msg, markup

    async def del_sending(self, code):
        async with connect(self.sql_path) as db:
            await db.execute('DELETE FROM sending WHERE photo = ?', [code])
            await db.commit()


class AdminButtons():
    def __init__(self) -> None:
        self.sql_path = './data/database.db'

    async def add_button(self, name, info, photo):
        async with connect(self.sql_path) as db:
            await db.execute('INSERT INTO buttons VALUES (?,?,?)', [name, info, photo])
            await db.commit()


    async def btn_menu_list(self):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM buttons')
            base = await select.fetchall()
        
        btn_list = []
        for i in base:
            btn_list.append(i[0])

        return btn_list


    async def info_buttons(self,name):
        async with connect(self.sql_path) as db:
            select = await db.execute(f'SELECT * FROM buttons WHERE name = ?', [name])
            info = await select.fetchone()
        info = list(info)

        return info

    async def buttons_markup(self):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM buttons')
            info = await select.fetchall()

        info = list(info)
        if len(info) > 0:
            markup = types.InlineKeyboardMarkup(row_width=2)
            x1 = 0
            x2 = 1
            for i in range(len(info)):
                try:
                    markup.add(
                        types.InlineKeyboardButton(text=f'🌀 {info[x1][0]} ', callback_data=f'info_btn:{info[x1][2]}'),
                        types.InlineKeyboardButton(text=f'🌀 {info[x2][0]} ', callback_data=f'info_btn:{info[x2][2]}')
                    )

                    x1 += 2
                    x2 += 2
                except:
                    try:
                        markup.add(
                            types.InlineKeyboardButton(text=f'🌀 {info[x1][0]}', callback_data=f'info_btn:{info[x1][2]}')
                        )
                    except:
                        return markup

            return markup

        else:
            return False

    async def btn_info(self, code):
        async with connect(self.sql_path) as db:
            select = await db.execute(f'SELECT * FROM buttons WHERE photo = ?', [code])
            info = await select.fetchone()

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add( 
            types.InlineKeyboardButton(text=f'Удалить', callback_data=f'del_btn:{code}'),
            types.InlineKeyboardButton(text=f'Выйти', callback_data=f'to_closed'),
        )

        msg = f"""
<b>🌀 Название кнопки:</b> {info[0]}
<b>🗒 Описание:</b>
{info[1]}
        """

        return msg, markup

    async def delete_button(self, code):
        async with connect(self.sql_path) as db:
            await db.execute('DELETE FROM buttons WHERE photo = ?', [code])
            await db.commit()    

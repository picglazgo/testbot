from aiosqlite import connect
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

from data import cheat_message
from utils import misc

class SMMPanel():
    def __init__(self) -> None:
        self.sql_path = './data/database.db'
        self.cheat = misc.cheat
        self.base = {
            'tg': 'Telegram',
            'vk': 'Vkontakte',
            'tt': 'TikTok',
            'yt': 'YouTube',
            'ig': 'Instagram',
            'ch': 'ClubHouse',
            'of': 'Onlifans',
            'sc': 'SoundCloud',
            'tw': 'Twitch',
            'lk': 'Likee',
            'ds': 'Discord',
        }

    def cheat_service_name(self, service):
        name = self.base.get(service)

        return name

    def cheat_type_name(self, cheat_types):
        types = {
            'subscriptions': 'Подписки',
            'views': 'Просмотры',
            'like': 'Лайки',
            'auditions': 'Прослушивания',
            'viewer': 'Зрители',
            'serv': 'Участники на сервер',
            'reactions': 'Реакции',
            'autoviews': 'Автопросмотры',
            'comments': 'Комментарии'
        }
        name = types.get(cheat_types)

        return name

    def cheat_order_name(self, service, cheat_type, order):
        orders = self.cheat.get(f'{service}').get(cheat_type)
        order_name = orders.get(order).get('name')

        return order_name

    async def cheating_menu(self):
        markup = types.InlineKeyboardMarkup(row_width=2)

        category = list(self.cheat.keys())

        x1 = 0
        x2 = 1

        for i in range(len(category)):
            try:
                markup.add(
                    types.InlineKeyboardButton(
                        text=f'{self.cheat_service_name(category[x1])}', callback_data=f'cheat_serivce:{category[x1]}'),
                    types.InlineKeyboardButton(
                        text=f'{self.cheat_service_name(category[x2])}', callback_data=f'cheat_serivce:{category[x2]}')
                )

                x1 += 2
                x2 += 2
            except IndexError:
                try:
                    markup.add(
                        types.InlineKeyboardButton(
                            text=f'{self.cheat_service_name(category[x1])}', callback_data=f'cheat_serivce:{category[x1]}'),
                    )
                    break
                except:pass

        markup.add(
                types.InlineKeyboardButton(text = 'Назад', callback_data = 'to_catalog'),
        )

        return markup



    async def cheat_logs(self, user_id, service, service_name, cheat_type, order_id, order_name, link, count, price_service, price):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT COUNT(*) FROM cheat_logs')
            count_logs = await select.fetchone()

            logs = [count_logs[0] + 1, user_id, service, service_name, cheat_type, order_id, order_name, count, price_service, price, link, datetime.now()]
            await db.execute('INSERT INTO cheat_logs VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', logs)
            await db.commit()

    async def user_cheatlogs_menu(self, user_id, page_number=1):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM cheat_logs WHERE user_id = ?', [user_id])
            logs = await select.fetchall()

        if len(logs) > 0:

            rows = 8
            page = []
            pages = []
            for i in logs:
                page.append(i)
                if len(page) == rows:
                    pages.append(page)
                    page = []

            if str(len(logs) / rows) not in range(16):
                pages.append(page)

            markup = types.InlineKeyboardMarkup(row_width=3)
            x1 = 0
            for i in range(int(len(pages[page_number-1]))):
                try:
                    markup.add(
                        types.InlineKeyboardButton(
                            text=f'📿 {pages[page_number-1][x1][3]} | {pages[page_number-1][x1][6]}', 
                            callback_data=f'my_cheat_logs:{pages[page_number-1][x1][0]}'),
                    )
                    x1 += 1
                except: pass

            previous_page_number = page_number + 1 if page_number == 1 else page_number - 1
            next_page_number = page_number + 1 if len(pages) > page_number else page_number
            if page_number == len(pages):
                previous_page_number = previous_page_number
                next_page_number = 1

            markup.add(
                types.InlineKeyboardButton(
                    text='ᐊ', callback_data=f'my_cheat_page:{previous_page_number}'),
                types.InlineKeyboardButton(
                    text=f'{page_number}/{len(pages)}', callback_data=f'pages_len_is'),
                types.InlineKeyboardButton(
                    text='ᐅ', callback_data=f'my_cheat_page:{next_page_number}'),
                types.InlineKeyboardButton(
                    text='Назад', callback_data='return_to_cabinet'),
            )
        else:
            markup = None

        return markup

    async def cheat_info_order(self, order_id):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM cheat_logs WHERE id = ?', [order_id])
            order_info = await select.fetchone()

        text = f"""
<b>💈 Cервис:</b> {order_info[3]} {self.cheat_type_name(order_info[4])}

<b>🧿 Название:</b> {order_info[6]}
<b>🧿 Количество:</b> {order_info[7]}

<b>🔗 Куда:</b> {order_info[10]}

<b>🕰 Дата заказа:</b> {order_info[11]}
        """
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(
                text='Назад', callback_data='return_to_cabinet')
        )

        return text, markup
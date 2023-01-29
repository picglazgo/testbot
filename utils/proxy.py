from states import user
from aiosqlite import connect
import requests, json, os
from aiogram import types
from datetime import datetime
from random import randint

from utils import config, misc, ProxyLine
from data import User, messages as mes
from . import CentralBankAPI


class Proxy:
    def __init__(self) -> None:
        self.sql_path = './data/database.db'
        self.days_list = [5, 10, 20, 30, 60, 90, 120, 150, 180, 
                    210, 240, 270, 300, 330, 360]
        self.proxy_count = [1, 2, 3, 4, 5, 10]
        self.country = misc.country
        self.city = misc.city

    def country_name(self, proxy_type, country_code):
        lists = self.country.get(proxy_type)
        name = lists.get(country_code)

        return name
    
    def city_name(self, country, city):
        index = self.city.get(country)
        name = index.get(int(city))

        return name

    def proxy_type_menu(self):
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(text='🌀 IPv4', callback_data='proxy_type:ipv4'),
            types.InlineKeyboardButton(text='🌐 IPv6', callback_data='proxy_type:ipv6'),
            types.InlineKeyboardButton(text='♻️ IPv4 Shared', callback_data='proxy_type:ipv4_shared'),
        )
        markup.add(
            types.InlineKeyboardButton(text='Выйти', callback_data='to_catalog')
        )

        return markup

    def proxy_time_menu(self, proxy_type):
        markup = types.InlineKeyboardMarkup(row_width=3)
        x1 = 0
        x2 = 1
        x3 = 2

        for i in range(6):
            try:
                markup.add(
                    types.InlineKeyboardButton(text = f'{self.days_list[x1]} дней', 
                                callback_data = f'proxy_time:{proxy_type}:{self.days_list[x1]}'),
                    types.InlineKeyboardButton(text = f'{self.days_list[x2]} дней', 
                                callback_data = f'proxy_time:{proxy_type}:{self.days_list[x2]}'),
                    types.InlineKeyboardButton(text = f'{self.days_list[x3]} дней', 
                                callback_data = f'proxy_time:{proxy_type}:{self.days_list[x3]}')
                )
                x1 += 3
                x2 += 3
                x3 += 3
            except IndexError:
                try:
                    markup.add(
                        types.InlineKeyboardButton(text = f'{self.days_list[x1]} дней', 
                                callback_data = f'proxy_time:{proxy_type}:{self.days_list[x1]}'),
                    )
                    break
                except:pass
        markup.add(
            types.InlineKeyboardButton(text = '🔙 Каталог', callback_data = 'to_catalog')
        )

        return markup

    def proxy_country_menu(self, proxy_type, proxy_time):
        country = list(self.country.get(proxy_type).keys())

        markup = types.InlineKeyboardMarkup(row_width=3)
        x1 = 0
        x2 = 1
        x3 = 2

        for i in range(len(country)):
            try:
                markup.add(
                    types.InlineKeyboardButton(text=f'{self.country_name(proxy_type, country[x1])}', 
                                            callback_data=f'proxy_country:{proxy_type}:{proxy_time}:{country[x1]}'),
                    types.InlineKeyboardButton(text=f'{self.country_name(proxy_type, country[x2])}', 
                                            callback_data=f'proxy_country:{proxy_type}:{proxy_time}:{country[x2]}'),
                    types.InlineKeyboardButton(text=f'{self.country_name(proxy_type, country[x3])}', 
                                            callback_data=f'proxy_country:{proxy_type}:{proxy_time}:{country[x3]}'),
                )
                x1 += 3
                x2 += 3
                x3 += 3
            except IndexError:
                try:
                    markup.add(
                        types.InlineKeyboardButton(text=f'{self.country_name(proxy_type, country[x1])}', 
                                            callback_data=f'proxy_country:{proxy_type}:{proxy_time}:{country[x1]}'),
                        types.InlineKeyboardButton(text=f'{self.country_name(proxy_type, country[x2])}', 
                                            callback_data=f'proxy_country:{proxy_type}:{proxy_time}:{country[x2]}'),
                    )
                    break
                except IndexError:
                    try:
                        markup.add(
                            types.InlineKeyboardButton(text=f'{self.country_name(proxy_type, country[x1])}', 
                                            callback_data=f'proxy_country:{proxy_type}:{proxy_time}:{country[x1]}'),
                        )
                        break
                    except:pass
        markup.add(
            types.InlineKeyboardButton(text='🔙 Меню', callback_data='to_catalog')
        )

        return markup
    
    def proxy_city_menu(self, proxy_type, proxy_time, proxy_country):
        city = list(self.city.get(proxy_country).keys())

        markup = types.InlineKeyboardMarkup(row_width=3)
        x1 = 0
        x2 = 1
        x3 = 2

        for i in range(len(city)):
            try:
                markup.add(
                    types.InlineKeyboardButton(text=f'{self.city_name(proxy_country, city[x1])}', 
                                            callback_data=f'proxy_city:{proxy_type}:{proxy_time}:{proxy_country}:{city[x1]}'),
                    types.InlineKeyboardButton(text=f'{self.city_name(proxy_country, city[x2])}', 
                                            callback_data=f'proxy_city:{proxy_type}:{proxy_time}:{proxy_country}:{city[x2]}'),
                    types.InlineKeyboardButton(text=f'{self.city_name(proxy_country, city[x3])}', 
                                            callback_data=f'proxy_city:{proxy_type}:{proxy_time}:{proxy_country}:{city[x3]}'),
                )
                x1 += 3
                x2 += 3
                x3 += 3
            except IndexError:
                try:
                    markup.add(
                        types.InlineKeyboardButton(text=f'{self.city_name(proxy_country, city[x1])}', 
                                            callback_data=f'proxy_city:{proxy_type}:{proxy_time}:{proxy_country}:{city[x1]}'),
                        types.InlineKeyboardButton(text=f'{self.city_name(proxy_country, city[x2])}', 
                                            callback_data=f'proxy_city:{proxy_type}:{proxy_time}:{proxy_country}:{city[x2]}'),
                    )
                    break
                except IndexError:
                    try:
                        markup.add(
                            types.InlineKeyboardButton(text=f'{self.city_name(proxy_country, city[x1])}', 
                                            callback_data=f'proxy_city:{proxy_type}:{proxy_time}:{proxy_country}:{city[x1]}'),
                        )
                        break
                    except:pass
        markup.add(
            types.InlineKeyboardButton(text='⛩ Любой город', 
                                    callback_data=f'proxy_city:{proxy_type}:{proxy_time}:{proxy_country}:0')
        )
        markup.add(
            types.InlineKeyboardButton(text='🔙 Меню', callback_data='to_catalog')
        )

        return markup

    def proxy_count_menu(self, proxy_type, proxy_time, proxy_country):
        markup = types.InlineKeyboardMarkup(row_width=3)
        x1 = 0
        x2 = 1
        x3 = 2

        for i in range(len(self.proxy_count)):
            try:
                markup.add(
                    types.InlineKeyboardButton(text = f'🧿 {self.proxy_count[x1]} Шт.', 
                                callback_data = f'proxy_сount:{proxy_type}:{proxy_time}:{proxy_country}:{self.proxy_count[x1]}'),
                    types.InlineKeyboardButton(text = f'🧿 {self.proxy_count[x2]} Шт.', 
                                callback_data = f'proxy_сount:{proxy_type}:{proxy_time}:{proxy_country}:{self.proxy_count[x2]}'),
                    types.InlineKeyboardButton(text = f'🧿 {self.proxy_count[x3]} Шт.', 
                                callback_data = f'proxy_сount:{proxy_type}:{proxy_time}:{proxy_country}:{self.proxy_count[x3]}')
                )
                x1 += 3
                x2 += 3
                x3 += 3
            except IndexError:
                try:
                    markup.add(
                        types.InlineKeyboardButton(text = f'🧿 {self.proxy_count[x1]} Шт.', 
                                callback_data = f'proxy_сount:{proxy_type}:{proxy_time}:{proxy_country}:{self.proxy_count[x1]}'),
                    )
                    break
                except:pass
        markup.add(
            types.InlineKeyboardButton(text = '🔙 Каталог', callback_data = 'to_catalog')
        )

        return markup

    async def get_prices(self, proxy_type, proxy_time, proxy_country, proxy_count):
        prices = await ProxyLine().get_price_proxy(proxy_type, proxy_country, proxy_count, proxy_time)
        currency = await CentralBankAPI().getCurrency()
        prices = float(currency) * prices
        price = prices / 100 * int(config.config("proxy_percent")) + prices

        return round(price)
    
    async def proxy_buy_info(self, proxy_type, proxy_time, proxy_country, proxy_count):
        price = await self.get_prices(proxy_type, proxy_time, proxy_country, proxy_count)
        if price != 0:
            text = f"""
<b>🧿 Вы выбрали:</b>

<b>💈 Тип:</b> {proxy_type}
<b>💈 Время:</b> {proxy_time} дней
<b>💈 Страна:</b> {self.country_name(proxy_type, proxy_country)}

<b>🔰 Количество:</b> {proxy_count} шт

<b>♻️ Цена:</b> {price} RUB

<b>✅ Для подтверждения покупки, нажмите кнопку «Купить» и ожидайте выдачу proxy.</b>
"""
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton(text=f'♻️ Купить | {price} RUB',
                                           callback_data=f'proxy_buy:{proxy_type}:{proxy_time}:{proxy_country}:{proxy_count}:{price}'),
                types.InlineKeyboardButton(text=f'🔝 Meню', callback_data = 'to_catalog'),
            )
        else:
            text = 'Технические неполадки, попробуйте чуть чуть позже'
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton(text=f'🔝 Meню', callback_data = 'to_catalog'),
            )

        return text, markup
    
    async def buy_proxy(self, bot, user_id, proxy_type, proxy_time, proxy_country, proxy_count, proxy_price, msg_id):
        await bot.delete_message(chat_id=user_id, message_id=msg_id)
        balance = await ProxyLine().get_balance()
        currency = await CentralBankAPI().getCurrency()
        balance = float(currency) * float(balance)
        if float(User(user_id).balance) >= float(proxy_price):
            if float(balance) >= float(proxy_price):
                order = await ProxyLine().new_order_proxy(proxy_type, proxy_country, proxy_count, proxy_time)
                price_service = await ProxyLine().get_price_proxy(proxy_type, proxy_country, proxy_count, proxy_time)
                if order[0] != 'NO_BALANCE':
                    await User(user_id).update_balance(-float(proxy_price))
                    await User(user_id).up_purchases(1)
                    msg = ''

                    for i in order:
                        text = f"""
<b>♻️ Тип прокси:</b> {i[4]} | {proxy_type}
<b>🌎 Страна:</b> {self.country_name(proxy_type, proxy_country)} 

<b>👨🏻‍💻 Логин:</b> <code>{i[7]}</code> | <b>Пароль:</b> <code>{i[8]}</code>

<b>🕰 Дата:</b> 
-покупки - {i[5]}  
-окончания - {i[6]}

<b>🌐 Proxy:</b> ip - <code>{i[0]}</code> | ID: {i[3]}

<b>🌀 Port:</b>
-http - <code>{i[9]}</code> |socks5 - <code>{i[10]}</code>

<b>🌐 Interval IP:</b> {i[11] if proxy_type == 'ipv6' else ''}
"""                 
                        msg += text

                        await self.write_history(user_id, i[12], i[3], proxy_type, proxy_country, 
                            i[0], i[9], i[10], i[7], i[8], datetime.now(), i[6], i[11] if proxy_type == 'ipv6' else '', price_service, proxy_price)
                    file_name = f'proxy_{randint(1111, 9999)}'

                    with open(file=f'./utils/docs/{file_name}.txt', mode='w+', encoding='UTF-8') as docs:
                        docs.write(msg)

                    with open(file=f'./utils/docs/{file_name}.txt', mode='rb') as docs:
                        await bot.send_message(chat_id=user_id, text=mes.access_purchase)
                    
                        await bot.send_document(chat_id=user_id, document=docs, caption='Ваши прокси  (^_^)')

                    product = open(f'./utils/docs/{file_name}.txt', 'rb')
                    text = f'Куплен товар!\n Пользователь: @{User(user_id).username} | {user_id}'
                    await bot.send_document(chat_id=config.config("admin_group"), document=product, caption=text)

                    os.remove(f'./utils/docs/{file_name}.txt')
                else:
                    await bot.send_message(chat_id=user_id, text='Технические неполадки!')
            else:
                await bot.send_message(chat_id=user_id, text='Технические неполадки!')
                await bot.send_message(chat_id=config.config("admin_group"), 
                    text=f'Пополни баланс проксилайн!\n Текущий баланс: {balance}| Цена покупки: {proxy_price}')
        
        else:
            await bot.send_message(chat_id=user_id, text='Пополните свой баланс!')
                

    async def write_history(self, user_id, order_id, proxy_id, proxy_type, country, ip, port_http, 
                    port_socks, user, password, data_buy, data_end, interval_ip, price_service, price):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT COUNT(*) FROM proxy_logs')
            count = await select.fetchone()

            proxy = [count[0] + 1, user_id, order_id, proxy_id, proxy_type, country, ip, port_http, 
                    port_socks, user, password, data_buy, data_end, f'{interval_ip}', price_service, price]

            await db.execute('INSERT INTO proxy_logs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', proxy)
            await db.commit()


    async def user_proxy_menu(self, user_id, page_number=1):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM proxy_logs WHERE user_id = ?', [user_id])
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
                            text=f'🧩{pages[page_number-1][x1][4]} | {self.country_name(pages[page_number-1][x1][4], pages[page_number-1][x1][5])}', 
                            callback_data=f'my_proxy_logs:{pages[page_number-1][x1][0]}'),
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
                    text='🌀 Активные прокси', callback_data=f'my_active_proxy'),
            )
            markup.add(
                types.InlineKeyboardButton(
                    text='ᐊ', callback_data=f'my_proxy_page:{previous_page_number}'),
                types.InlineKeyboardButton(
                    text=f'{page_number}/{len(pages)}', callback_data=f'pages_len_is'),
                types.InlineKeyboardButton(
                    text='ᐅ', callback_data=f'my_proxy_page:{next_page_number}'),
                types.InlineKeyboardButton(
                    text='Назад', callback_data='return_to_cabinet'),
            )
        else:
            markup = None

        return markup

    async def user_act_proxy_menu(self, user_id, page_number=1):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM proxy_logs WHERE user_id = ?', [user_id])
            logs = await select.fetchall()

        act_proxy = []
        for i in logs:
            if datetime.fromisoformat(i[12].split("+")[0]) > datetime.now():
                act_proxy.append(i)

        if act_proxy != []:

            rows = 8
            page = []
            pages = []
            for i in act_proxy:
                page.append(i)
                if len(page) == rows:
                    pages.append(page)
                    page = []

            if str(len(act_proxy) / rows) not in range(16):
                pages.append(page)

            markup = types.InlineKeyboardMarkup(row_width=3)
            x1 = 0
            for i in range(int(len(pages[page_number-1]))):
                try:
                    markup.add(
                        types.InlineKeyboardButton(
                            text=f'🧩{pages[page_number-1][x1][4]} | {self.country_name(pages[page_number-1][x1][4], pages[page_number-1][x1][5])}', 
                            callback_data=f'my_act_proxy:{pages[page_number-1][x1][0]}'),
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
                    text='ᐊ', callback_data=f'act_proxy_page:{previous_page_number}'),
                types.InlineKeyboardButton(
                    text=f'{page_number}/{len(pages)}', callback_data=f'pages_len_is'),
                types.InlineKeyboardButton(
                    text='ᐅ', callback_data=f'act_proxy_page:{next_page_number}'),
                types.InlineKeyboardButton(
                    text='Назад', callback_data='return_to_cabinet'),
            )
        else:
            markup = None

        return markup
    
    async def user_info_order(self, logs_id):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM proxy_logs WHERE id = ?', [logs_id])
            order_info = await select.fetchone()

        text = f"""
<b>♻️ Тип прокси:</b> {order_info[4]}
<b>🌎 Страна:</b> {self.country_name(order_info[4], order_info[5])} 

<b>👨🏻‍💻 Логин:</b> <code>{order_info[9]}</code> | <b>Пароль:</b> <code>{order_info[10]}</code>

<b>🕰 Дата:</b> 
-покупки - {order_info[11]}  
-окончания - {order_info[12]}

<b>🌐 Proxy IP:</b>- <code>{order_info[6]}</code>

<b>🌀 Port:</b>
-http - <code>{order_info[7]}</code> |socks5 - <code>{order_info[8]}</code>

<b>🌐 Interval IP:</b> {order_info[13]}
        """
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(
                text='Назад', callback_data='return_to_cabinet')
        )

        return text, markup

    async def user_info_act_order(self, logs_id):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM proxy_logs WHERE id = ?', [logs_id])
            order_info = await select.fetchone()

        text = f"""
<b>♻️ Тип прокси:</b> {order_info[4]}
<b>🌎 Страна:</b> {self.country_name(order_info[4], order_info[5])} 

<b>👨🏻‍💻 Логин:</b> <code>{order_info[9]}</code> | <b>Пароль:</b> <code>{order_info[10]}</code>

<b>🕰 Дата:</b> 
Покупки: {order_info[11]}  
Oкончания: {order_info[12].split("+")[0]}

<b>🌐 Proxy IP:</b>- <code>{order_info[6]}</code>

<b>🌀 Port:</b>
http: <code>{order_info[7]}</code> | socks5: <code>{order_info[8]}</code>

<b>🌐 Interval IP:</b> <code>{order_info[13]}</code> 
        """
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(
                text='♻️ Продлить прокси', callback_data=f'renew_proxy:{order_info[2]}:{logs_id}')
        )
        markup.add(
            types.InlineKeyboardButton(
                text='Назад', callback_data='return_to_cabinet')
        )

        return text, markup

    def renew_proxy_time(self, order_id, logs_id):
        markup = types.InlineKeyboardMarkup(row_width=3)
        x1 = 0
        x2 = 1
        x3 = 2

        for i in range(6):
            try:
                markup.add(
                    types.InlineKeyboardButton(text=f'{self.days_list[x1]} дней', 
                                callback_data=f'renew_proxy_time:{order_id}:{self.days_list[x1]}'),
                    types.InlineKeyboardButton(text=f'{self.days_list[x2]} дней', 
                                callback_data=f'renew_proxy_time:{order_id}:{self.days_list[x2]}'),
                    types.InlineKeyboardButton(text=f'{self.days_list[x3]} дней', 
                                callback_data=f'renew_proxy_time:{order_id}:{self.days_list[x3]}')
                )
                x1 += 3
                x2 += 3
                x3 += 3
            except IndexError:
                try:
                    markup.add(
                        types.InlineKeyboardButton(text=f'{self.days_list[x1]} дней', 
                                callback_data=f'renew_proxy_time:{order_id}:{self.days_list[x1]}'),
                    )
                    break
                except:pass
        markup.add(
            types.InlineKeyboardButton(text='Назад', callback_data=f'my_act_proxy:{logs_id}')
        )

        return markup

    async def renew_proxy_info(self, order_id, time):
        async with connect(self.sql_path) as db:
            select = await db.execute('SELECT * FROM proxy_logs WHERE order_id = ?', [order_id])
            order_info = await select.fetchone()

        price = await self.get_prices(order_info[4], time, order_info[5], 1)
        service_price = await ProxyLine().get_price_proxy(order_info[4], order_info[5], 1, time)
        if price != 0:
            text = f"""
<b>🧿 Продление прокси:</b>

<b>💈 Тип:</b> {order_info[4]}
<b>💈 Страна:</b> {self.country_name(order_info[4], order_info[5])}

<b>🔰 Продлить на:</b> {time} дней

<b>♻️ Цена:</b> {price} RUB

<b>✅ Для подтверждения покупки, нажмите кнопку «Продлить» и ожидайте продления.</b>
"""
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton(text=f'♻️ Продлить | {price} RUB',
                                           callback_data=f'proxy_renew:{order_id}:{time}:{price}:{service_price}'),
            )
            markup.add(
                types.InlineKeyboardButton(text='Назад', callback_data=f'renew_proxy:{order_id}:{order_info[0]}'),
                types.InlineKeyboardButton(text=f'🔝 Выйти', callback_data = 'return_to_cabinet'),
            )
        else:
            text = 'Технические неполадки, попробуйте чуть чуть позже'
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton(text=f'🔝 Выйти', callback_data = 'return_to_cabinet'),
            )

        return text, markup

    async def proxy_renew_order(self, bot, user_id, order_id, time, price, service_price):
        user = User(user_id)
        if float(user.balance) >= float(price):
            balance = await ProxyLine().get_balance()
            if float(balance) >= float(price):
                order = await ProxyLine().renew_proxy_order(order_id, time)
                print(order)
                if order[0] != 'ERRORS':
                    text = f"""
<b>♻️ Тип прокси:</b> ipv{order[4]}
<b>🌎 Страна:</b> {self.country_name(f'ipv{order[4]}', order[1])} 

<b>👨🏻‍💻 Логин:</b> <code>{order[7]}</code> | <b>Пароль:</b> <code>{order[8]}</code>

<b>🕰 Дата:</b> 
-покупки - {order[5]}  
-окончания - {order[6]}

<b>🌐 Proxy:</b> ip - <code>{order[0]}</code> | ID: {order[3]}

<b>🌀 Port:</b>
-http - <code>{order[9]}</code> |socks5 - <code>{order[10]}</code>

<b>🌐 Interval IP:</b> {order[11] if order[4] == '6' else ''}
                    """
                    async with connect(self.sql_path) as db:
                        await db.execute('UPDATE proxy_logs SET data_end = ? WHERE order_id = ?', [f'{datetime.now()}+03:00', order_id])
                        await db.commit()

                    await self.write_history(user_id, order[12], order[3], order[4], order[1], order[0], order[9], 
                        order[10], order[7], order[8], order[5], order[6], order[11], service_price, price)
                else:
                    text = 'Технические неполадки!'
            else:
                text = 'Технические неполадки!'
                await bot.send_message(chat_id=config.config("admin_group"), 
                    text=f'Пополни баланс проксилайн!\n Текущий баланс: {balance}| Цена покупки')

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
                types.InlineKeyboardButton(text=f'🔝 Выйти', callback_data = 'return_to_cabinet'),
        )
        return text, markup




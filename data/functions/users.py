# © copyright by VoX DoX
import sqlite3
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, date
from typing import Tuple

import requests

from . import AioSQL


class User(AioSQL):
    """
    User: классс SQL для работы с
    пользователями
    """
    def __init__(self,
                 user_id: int = None) -> None:
        super().__init__()
        if user_id is not None:
            self.sql_path = './data/database.db'
            conn = sqlite3.connect(self.sql_path)
            cursor = conn.cursor()

            cursor.execute(f'SELECT * FROM users WHERE user_id = ?', [user_id])
            user = cursor.fetchone()

            self.user_id = user[0]
            self.username = user[1]
            self.status = user[2]
            self.balance = user[3]
            self.purchases = user[4]
            self.who_invite = user[5]
            self.date = user[6]
            self.ban = user[7]
            self.refBalance = user[8]


    async def addPunshare(self, category, name, text):
        await self.__ainit__()
        await self.db.execute('INSERT INTO purchase_history VALUES(?,?,?,?)', [self.user_id, category, name, text, datetime.now()])
        await self.conn.commit()


    async def getStatus(self, id):
        await self.__ainit__()
        await self.db.execute('SELECT status FROM users WHERE user_id=?', [id])
        return await self.db.fetchone()


    async def getBtcBalance(self):
        res = requests.get('https://blockchain.info/ticker').json()
        result = round(float(self.balance) / res['RUB']['15m'] , 8) 
        return result


    async def updateBalance(self,
                            value: float) -> None:
        """
        Обновление баланса пользователю
        :param value: float
        :return: None
        """
        await self.__ainit__()

        await self.db.execute(
            "UPDATE users SET balance = ? WHERE user_id = ?",
            [float(self.balance) + float(value), self.user_id]
        )
        await self.conn.commit()

    async def updatePurchases(self,
                              value: int) -> None:
        """
        Изменение кол-во покупок для пользователя
        :param value:
        :return:
        """
        await self.__ainit__()

        await self.db.execute(
            'UPDATE users SET purchases = ? WHERE user_id = ?',
            [self.purchases + value, self.user_id]
        )
        await self.conn.commit()

    async def updateStatusBan(self,
                              value: str) -> None:
        """
        Обновление статуса бана для
        пользователя
        :param value: str
        :return: None
        """
        await self.__ainit__()

        await self.db.execute(
            'UPDATE users SET ban = ? WHERE user_id = ?',
            [value, self.user_id]
        )
        await self.conn.commit()

    async def updateFullBalance(self,
                                value: float) -> None:
        """
        Полное изменение баланса для
        пользователя
        :param value: float
        :return: None
        """
        await self.__ainit__()

        await self.db.execute(
            'UPDATE users SET balance = ? WHERE user_id = ?',
            [value, self.user_id]
        )
        await self.conn.commit()

    async def writeRefferalProfit(self,
                                  amount: float) -> None:
        """
        Запись лога о реф программе и заработке
        :param amount: float
        :return: None
        """
        await self.__ainit__()

        await self.db.execute(
            'INSERT INTO refferal_logs VALUES (?,?,?)',
            [self.user_id, amount, datetime.now()]
        )
        await self.conn.commit()

    def get_days(self):
        join_time = self.date[:10].split('-')
        pars_time = date(int(join_time[0]), int(join_time[1]), int(join_time[2]))
        today = date.today()
        delta = today - pars_time
        day = str(delta).split()[0]
        if day.split(':')[0] == '0':
            day = 1

        return day

    async def checkFromBase(self,
                            user_id: int) -> bool:
        """
        Проверка на наличие пользователя в базе
        :param user_id: int
        :return: bool
        """
        await self.__ainit__()

        await self.db.execute(
            "SELECT * FROM users WHERE user_id = ?", [user_id]
        )
        data = await self.db.fetchall()

        if len(data) > 0:
            return True

        return False

    async def joinFromBot(self,
                          user_id: int,
                          username: str,
                          who_invite) -> Tuple[bool, int]:
        """
        Проверка и запись пользователя в
        базу данных
        :param user_id: int
        :param username: str
        :param who_invite:
        :return: Tuple[bool, int]
        """
        await self.__ainit__()

        status, who_in, userStatus = False, 0, ''

        info = await self.db.execute(
            "SELECT * FROM users WHERE user_id = ?", [user_id]
        )
        select = await info.fetchall()

        if who_invite != '':
            who_in = who_invite

            who = await self.db.execute(
                "SELECT * FROM users WHERE user_id = ?", [who_in]
            )
            invite = await who.fetchall()

            if len(invite) == 0:
                who_in = 0

        if len(select) == 0:
            await self.db.execute(
                "INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?)",
                [user_id, f"{username}", 'step1', 0, 0, who_invite, datetime.now(), 'no', 0]
            )
            await self.conn.commit()
            status = True
            userStatus = 'step1'
        else:
            userStatus = select[0][2]

        return status, who_in, userStatus

    async def updateStatus(self, user_id, status):
        await self.__ainit__()
        await self.db.execute('UPDATE users SET status=? WHERE user_id=?', [status, user_id])
        await self.conn.commit()

    async def getCountRefferal(self) -> int:
        """
        Получаем количество рефов
        у юзера
        :param user_id: int
        :return: int
        """
        await self.__ainit__()

        await self.db.execute(
            'SELECT * FROM users WHERE who_invite = ?', [self.user_id]
        )
        refferal = await self.db.fetchall()

        return len(refferal)


    async def getPurchases(self):
        await self.__ainit__()
        select = await self.db.execute(
            'SELECT * FROM purchase_history WHERE user_id = ?', [self.user_id]
        )
        return await select.fetchall()


    async def purchases_history(self) -> InlineKeyboardMarkup:
        await self.__ainit__()
        select = await self.db.execute(
            'SELECT * FROM purchase_history WHERE user_id = ?', [self.user_id]
        )
        info = await select.fetchall()

        product = list(info)
        markup = InlineKeyboardMarkup(row_width=2)
        x1 = 0
        x2 = 1

        for i in range(len(product)):
            try:
                markup.add(
                    InlineKeyboardButton(
                        text=f'{product[x1][3]}', callback_data=f'user_purchase:{product[x1][0]}'
                    ),
                    InlineKeyboardButton(
                        text=f'{product[x2][3]}', callback_data=f'user_purchase:{product[x2][0]}'
                    )
                )

                x1 += 2
                x2 += 2
            except IndexError:
                try:
                    markup.add(
                        InlineKeyboardButton(
                            text=f'{product[x1][3]}', callback_data=f'user_purchase:{product[x1][0]}'
                        ),
                    )
                    break
                except IndexError:
                    pass
        markup.add(
            InlineKeyboardButton(
                text='Назад', callback_data='return_to_cabinet'
            )
        )
        return markup

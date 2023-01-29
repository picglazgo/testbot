from aiohttp import ClientSession
from json import loads
from typing import Union


class WiqAPI:
    def __init__(self):
        self._API_ = ""
        self._BASE_URL_ = "https://wiq.ru/api/"

    async def __response(self,
                         data: dict):
        """
                Закидываем запрос на API с нужными нам запросами
                :param data: dict
                :return:
        """
        async with ClientSession() as session:
            async with session.post(url=self._BASE_URL_, data=data) as response:
                if response.status == 200:
                    answer = await response.text()

                    return answer

        return "ERROR"

    async def getBalance(self) -> Union[float, int]:
        """
        Возвращает баланс на панели
        :return: Union[float, int]
        """
        data = {
            "key": self._API_,
            "action": "balance"
        }
        response = await self.__response(data=data)
        if response != "ERROR":
            answer: dict = loads(response)
            balance: float = answer['balance']

            return balance

        return 0

    async def getServices(self) -> Union[dict, bool]:
        """
        Возвращает словарь со всеми сервисами накрутки
        :return: Union[dict, bool]
        """
        data = {
            "key": self._API_,
            "action": "services"
        }
        response = await self.__response(data=data)
        if response != "ERROR":
            answer: dict = loads(response)

            return answer

        return False

    async def getRefill(self,
                        order_id: int) -> Union[str, bool]:
        """
        Запрос восстановления отписок,
        возвращает статус с сервиса
        :param order_id: int
        :return: Union[str, bool]
        """
        data = {
            "key": self._API_,
            "action": "refill",
            "order": order_id
        }
        response = await self.__response(data=data)
        if response != "ERROR":
            answer: dict = loads(response)

            return answer['status']

        return False

    async def getCancel(self,
                        order_id: int) -> Union[str, bool]:
        """
        Отмена заказа накрутки, возвращает статус
        :param order_id: int
        :return: Union[str, bool]
        """
        data = {
            "key": self._API_,
            "action": "cancel",
            "order": order_id
        }
        response = await self.__response(data=data)
        if response != "ERROR":
            answer: dict = loads(response)

            return answer['status']

        return False

    async def getStatus(self,
                        order_id: int) -> Union[dict, bool]:
        """
        Получение статуса заказа
        Возвращает словарь, с информацией об заказе
        :param order_id: int
        :return: Union[dict, bool]
        """
        data = {
            "key": self._API_,
            "action": "status",
            "order": order_id
        }
        response = await self.__response(data=data)
        if response != "ERROR":
            answer: dict = loads(response)

            return answer

        return False

    async def createOrder(self,
                          order_id: int,
                          quantity: int,
                          link: str,
                          posts: int = None) -> Union[int, bool]:
        """
        Заказ накрутки, возвращает айди заказа
        :param order_id: int
        :param quantity: int
        :param link: str
        :param posts: int
        :return: Union[int, bool]
        """
        data = {
            "key": self._API_,
            "action": "create",
            "service": order_id,
            "quantity": quantity,
            "link": link,
        }
        if posts is not None:
            data['posts'] = posts

        response = await self.__response(data=data)
        if response != "ERROR":
            answer: dict = loads(response)

            return answer['order']

        return False

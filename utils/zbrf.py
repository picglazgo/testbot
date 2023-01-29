import requests
from json import loads
from bs4 import BeautifulSoup


class CentralBankAPI:
    def __init__(self):
        self.__BASE_URL = 'https://www.cbr.ru/scripts/XML_daily.asp'

        self.currency_id = {
            "USD": "R01235",
            "EUR": "R01239",
            "KZT": "R01335",
        }

    async def getCurrency(self, currency: str = "USD") -> float:
        currency = self.currency_id.get(currency)
        response = requests.get(url=self.__BASE_URL)

        soup = BeautifulSoup(response.content, 'xml')
        find_currency = soup.find(ID=currency).Value.string
        curse = find_currency.replace(',', '.')

        return curse

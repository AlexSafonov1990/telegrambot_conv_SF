import requests
import json
from config import currency_dict, APIKEY

class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты: {quote}')

        try:
            quote_ticker = currency_dict[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {quote}')

        try:
            base_ticker = currency_dict[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество: {amount}')

        payload = {}
        headers = {
            "apikey": APIKEY
        }

        response = requests.get(
            f"https://api.apilayer.com/exchangerates_data/convert?to={base_ticker}&from={quote_ticker}&amount={amount}",
            headers=headers, data=payload
        )

        text = json.loads(response.content).get("result")

        return text

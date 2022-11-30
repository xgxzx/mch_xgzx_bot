import requests
import json
from config import keys


class ConvertingException(Exception):
    pass


class Converter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertingException('Нужно указать разные валюты')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertingException(f'Не знаю валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertingException(f'Не знаю валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertingException(f'Не верное количество {amount}')

        r = requests.get(f'https://api.coingate.com/v2/rates/merchant/{quote_ticker}/{base_ticker}')
        total = json.loads(r.content) * float(amount)

        return total

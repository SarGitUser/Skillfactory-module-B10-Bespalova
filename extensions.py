import requests
import json
from config import exchanges

class APIException(Exception):  # наши исключения с пояснением ошибки со стороны пользователя (неправильный ввод...)
    pass

class CryptoConverter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            quote_key = exchanges[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        url = f"https://api.apilayer.com/exchangerates_data/latest?base={base_key}&symbols={quote_key}"   # валюту введет пользователь через бота
        payload = {}
        headers = {"apikey": "YrYIGPtrt4zM3LslTowWJS0Crfi2E7EJ"}
        response = requests.request("GET", url, headers=headers, data=payload)
        resp = json.loads(response.content)
        new_price = resp['rates'][quote_key] * float(amount)
        return round(new_price, 3)

import requests


class RealTimeCurrencyConverter:
    def __init__(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверить на ошибки HTTP
            self.data = response.json()
            self.currencies = self.data['rates']
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении данных: {e}")
            self.currencies = None

    def convert(self, from_currency, to_currency, amount):
        if self.currencies is None:
            return None  # Возвращать None, если данные не были получены

        initial_amount = amount
        if from_currency != 'USD':
            try:
                amount = amount / self.currencies[from_currency]
            except KeyError:
                print(f"Ошибка: Неверная исходная валюта: {from_currency}")
                return None

        try:
            amount = round(amount * self.currencies[to_currency], 4)
        except KeyError:
            print(f"Ошибка: Неверная целевая валюта: {to_currency}")
            return None

        return amount


def get_exchange_rate(converter, to_currency='RUB'):
    """Получает курс USD к указанной валюте."""
    if converter.currencies is None:
        return None
    try:
        return converter.currencies[to_currency]
    except KeyError:
        print(f"Ошибка: Неверная валюта: {to_currency}")
        return None


if __name__ == "__main__":
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    converter = RealTimeCurrencyConverter(url)

    if converter.currencies is None:
        print("Приложение не может работать из-за ошибки при получении данных.")
    else:
        exchange_rate = get_exchange_rate(converter, 'RUB')

        if exchange_rate is not None:
            print(f"Текущий курс: 1 USD = {exchange_rate:.4f} RUB")

            while True:
                try:
                    rub_amount = float(input("Введите сумму в рублях: "))
                    if rub_amount < 0:
                        print("Сумма должна быть неотрицательной")
                        continue
                    break
                except ValueError:
                    print("Некорректный ввод. Пожалуйста, введите число.")

            usd_amount = converter.convert('RUB', 'USD', rub_amount)

            if usd_amount is not None:
                print(f"{rub_amount:.2f} рублей = {usd_amount:.2f} долларов")
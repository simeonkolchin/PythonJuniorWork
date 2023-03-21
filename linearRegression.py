import ccxt
import numpy as np
import time
from sklearn.linear_model import LinearRegression

exchange = ccxt.binance({
    'enableRateLimit': True,
})

symbol = 'ETH/USDT'
limit = 120  # количество минут для анализа цены


def fetch_ohlcv(exchange, symbol, timeframe, limit):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    return ohlcv


def analyze_price():
    # Получаем данные о цене ETHUSDT и BTCUSDT за последние 60 минут
    ethusdt_data = fetch_ohlcv(exchange, 'ETH/USDT', '1m', limit=60)
    btcusdt_data = fetch_ohlcv(exchange, 'BTC/USDT', '1m', limit=60)

    # Извлекаем только столбец цены из данных о цене
    ethusdt_price = np.array([data[4] for data in ethusdt_data]).reshape(-1, 1)
    btcusdt_price = np.array([data[4] for data in btcusdt_data]).reshape(-1, 1)

    # Вычисляем коэффициенты линейной регрессии
    reg = LinearRegression().fit(btcusdt_price, ethusdt_price)

    # Вычисляем собственные движения цены ETHUSDT, вычитая из текущей цены предсказанную цену на основе уравнения регрессии
    ethusdt_predicted_price = reg.predict(btcusdt_price)[-1][0]
    ethusdt_current_price = ethusdt_price[-1][0]
    ethusdt_movement = ethusdt_current_price - ethusdt_predicted_price

    # Возвращаем собственные движения цены ETHUSDT
    return ethusdt_movement


def check_price_change():
    # Получаем данные о цене ETHUSDT за последние 60 минут
    ethusdt_data = fetch_ohlcv(exchange, 'ETH/USDT', '1m', limit=60)

    # Извлекаем только столбец цены из данных о цене
    ethusdt_price = np.array([data[4] for data in ethusdt_data]).reshape(-1, 1)

    # Вычисляем процентное изменение цены за последние 60 минут
    price_change = (ethusdt_price[-1][0] - ethusdt_price[0][0]) / ethusdt_price[0][0]

    # Проверяем, было ли изменение цены больше или равно 1%
    if abs(price_change) >= 0.01:
        # Выводим сообщение в консоль
        print(f"Изменение цены: {price_change * 100:.2f}% в последнии 60 минут.")


while True:
    # Вызываем функцию analyze_price() для вычисления собственных движений цены ETHUSDT
    ethusdt_movement = analyze_price()
    # Выводим собственные движения цены ETHUSDT в консоль
    print(f"Движения ETHUSDT: {ethusdt_movement:.2f}")

    # Проверяем изменение цены ETHUSDT за последние 60 минут
    check_price_change()

    # Задерживаем выполнение программы на 1 минуту
    time.sleep(60)

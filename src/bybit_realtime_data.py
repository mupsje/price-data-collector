from pybit import HTTP, WebSocket
from datetime import datetime
from price import Price
import postgresql
import json
import time


def current_timestamp():
    return int(datetime.now().timestamp())


def open_bybit_socket(symbol, interval):
    ws = WebSocket(
        endpoint='wss://stream.bybit.com/realtime',
        subscriptions=[f'klineV2.{interval}.{symbol}'],
        api_key=None,
        api_secret=None
    )
    return ws


def write_prices_to_log(prices):
    with open("../Bybit-BTCUSD-realtime-prices.csv", "a") as log:
        for entry in prices:
            log.write(entry.__str__() + "\n")

if __name__ == "__main__":
    prices = []
    symbol = 'BTCUSD'
    interval = '1'

    ws = open_bybit_socket(symbol, '1')

    while 1:
        price_data = ws.fetch('klineV2.1.BTCUSD')
        if price_data:
            prices.append(
                Price(price_data['close'], current_timestamp(), symbol))
            if(len(prices) > 60):
                write_prices_to_log(prices)
                prices.clear()
            else:
                time.sleep(1)  # Delay for 1 minute (60 seconds).

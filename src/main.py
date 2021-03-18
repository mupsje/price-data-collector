from multiprocessing import Process
from pybit import HTTP, WebSocket
from datetime import datetime
from price import Price
from database import DB
import os
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

def collect_data(symbol: str, interval:str):
    print('Starting the price collection for {}'.format(symbol))
    prices = []
    
    database = DB(os.environ['DBHOST'], os.environ['DBNAME'],os.environ['DBUSERNAME'],os.environ['DBPASSWORD'])
    database.create_prices_table(symbol)

    ws = open_bybit_socket(symbol, interval)
    
    while 1:
        price_data = ws.fetch('klineV2.1.{}'.format(symbol))
        if price_data:
            prices.append(Price(price_data['close'], current_timestamp(), symbol))
            if(len(prices) > 60):
                database.batch_insert_prices(symbol,prices)
                prices.clear()
            else:
                time.sleep(1) 

if __name__ == "__main__":
    connections_variables = ['DBHOST','DBNAME', 'DBUSERNAME', 'DBPASSWORD']
    for parameter in connections_variables:
        if os.environ.get(parameter) is None:
            print('The environment variable "{}" must be present in order to connection to the database'.format(parameter))
            raise Exception("Missing environment variable {}".format(parameter))

    interval = '1'
    symbols = ['BTCUSD', 'ETHUSD']
    processes = []

    for symbol in symbols:
        process = Process(target=collect_data, args=(symbol,interval))
        process.start()
        processes.append(process)
        time.sleep(12)
    
    for process in processes:
        process.join()
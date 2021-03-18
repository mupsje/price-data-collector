import psycopg2
import psycopg2.extras
from price import Price


class DB:
    def __init__(self, host:str, db_name:str, username:str, password:str):
        print('Establishing connection with postgresql')
        self.connection = psycopg2.connect(
            host=host,
            database=db_name,
            user=username,
            password=password,
        )
        self.connection.autocommit = True

    def create_prices_table(self, symbol):
        print('Creating table', symbol, 'if not present to store price data')
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS {}(time timestamp NOT NULL PRIMARY KEY, price float8 NOT NULL);
                """.format(symbol))


    # Insert a batch of prices all at once on postgresql
    def batch_insert_prices(self, symbol: str, prices:list[Price]) -> None:
        insertList = [[p.timestamp, p.value] for p in prices]
        with self.connection.cursor() as cursor:
            psycopg2.extras.execute_batch(cursor, 'INSERT INTO {} VALUES (to_timestamp(%s), %s) ON CONFLICT DO NOTHING;'.format(symbol), insertList)

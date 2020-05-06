from DBcm3 import UseDatabase, ConnectionError, CredentialsError, SQLError

from datetime import date, datetime
import time


# configuration for database
dbConfig = {'host' : '127.0.0.1',
            'user' : 'tradingBot',
            'password' : '1234',
            'database' : 'trading'}

def write_order(order) -> dict:
    mDate = datetime.utcfromtimestamp(order.date).strftime('%Y-%m-%d %H:%M:%S')
    _SQL = "INSERT INTO orders (date, type, pair, side, price, amount, filled, total, fee) value ('" + mDate + "', "
    _SQL += order[]
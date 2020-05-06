# from NtpUpdateTime import update_time
import time
from datetime import datetime
import math

from binance import client
from binance.enums import *
from pyrogram import Client



class Account():
    def __init__(self, name, phone_number, t_api_id, t_api_hash, b_api_key, b_secret_key, message_text, channel_id):
        self.name = name
        self.phone_number = phone_number
        self.t_api_id = t_api_id
        self.t_api_hash = t_api_hash
        self.b_api_key = b_api_key
        self.b_secret_key = b_secret_key
        self.binance_acc = self.get_binance_client()
        self.message_text = message_text
        self.channel_id = channel_id
        self.log = ""

        self.app = Client('my-session', phone_number = self.phone_number, api_id = self.t_api_id, api_hash = self.t_api_hash)
        self.app.start()
        self.app.send_message(chat_id = self.channel_id, text = "Start working")

    def __str__(self):
        return self.name + ", " + self.phone_number

    def get_binance_client(self):
        return client.Client(self.b_api_key, self.b_secret_key)

    #checking for existing an opened stoploss order
    def get_stoploss(self, my_order: dict) -> float:
        all_orders = self.binance_acc.get_all_orders(symbol = my_order["symbol"])
        stoploss = [order for order in all_orders
                        if order["orderId"] > my_order["orderId"]
                        and order["type"] == "STOP_LOSS"
                        and order["origQty"] == my_order["origQty"]
                        ]
        return stoploss

    def get_OCO(self, my_order: dict) -> float:
        all_orders = self.binance_acc.get_all_orders(symbol = my_order["symbol"])
        OCO = [order for order in all_orders
                        if order["orderId"] > my_order["orderId"]
                        and order["type"] == "OCO"
                        and order["origQty"] == my_order["origQty"]
                        ]
        return OCO

    # calculate stoploss
    def calc_stoploss(self, order_stat: dict) -> float:
        prices = self.binance_acc.get_order_book(symbol = order_stat["symbol"], limit = 10)
        min_price = float(prices["asks"][0][0])
        my_price = float(order_stat["price"])
        coin_info = self.binance_acc.get_symbol_info(symbol = order_stat["symbol"])
        tick_size = float(coin_info["filters"][0]["tickSize"])
        if  my_price*0.9 <= min_price < my_price*1.05:
            stoploss = math.floor(round(my_price*0.9,8)/tick_size)*tick_size
        elif my_price*1.05 <= min_price:
            stoploss = math.floor(round(min_price*0.96,8)/tick_size)*tick_size
        else:
            stoploss = min_price
        return stoploss

    #calculating the value of deposit in BTC
    def calculate_btc_equivalent_depo(self) -> float:
        acc_info = self.binance_acc.get_account()
        balances = acc_info["balances"]
        not_null_balances = {coin["asset"]: float(coin["free"])+float(coin["locked"]) for coin in balances if float(coin["free"])+float(coin["locked"]) > 0} #getting not null balance coins
        estimated_value = 0

        # for all not null balace coins calculating and summing value in BTC
        for coin, free in not_null_balances.items():
            try:
                if not coin == "BTC":
                    coin_order_book = self.binance_acc.get_order_book(symbol=coin + "BTC", limit=10)
                    min_price = coin_order_book["bids"][0][0]
                    estimated_value += float(min_price) * free
                else:
                    estimated_value += free

            except Exception as err:
                print(err)
                print((coin, free))
                self.log += "calculate_depo error:" + err.__str__() + "coin, free = " + str((coin, free)) + "\n"
                continue

        return estimated_value

    #getting the minimum price(ask) in order book
    def get_coin_price(self, coin: str) -> float:
        order_book = self.binance_acc.get_order_book(symbol = coin)
        return order_book['asks'][0][0]

    #calculating the value of deposit in BTC
    def calculate_depo(self) -> float:
        acc_info = self.binance_acc.get_account()
        balances = acc_info["balances"]
        not_null_balances = {coin["asset"]: float(coin["free"])+float(coin["locked"]) for coin in balances if float(coin["free"])+float(coin["locked"]) > 0} #getting not null balance coins
        estimated_value = 0

        # for all not null balace coins calculating and summing value in BTC
        for coin, free in not_null_balances.items():
            try:
                if not coin == "BTC":
                    coin_order_book = self.binance_acc.get_order_book(symbol=coin + "BTC", limit=10)
                    min_price = coin_order_book["bids"][0][0]
                    estimated_value += float(min_price) * free
                else:
                    estimated_value += free

            except Exception as err:
                print(err)
                print((coin, free))
                self.log += "calculate_depo error:" + err.__str__() + "coin, free = " + str((coin, free)) + "\n"
                continue

        return estimated_value

    def get_BTC_balance(self) -> float:
        acc_info = self.binance_acc.get_account()
        return float(acc_info["balances"][0]["free"])

    #calculate lot size, two options - 10 percent of all budget, or min notional
    def calculate_lot_size(self, symbol: str, price: str) -> int:
        # calculating the general deposit of the account
        #depo = self.calculate_depo()
        #lot_size_depo = (depo * 0.1) if self.get_BTC_balance() > (depo * 0.1) else self.get_BTC_balance()
        lot_size_depo = self.get_BTC_balance()
        symbol_info = self.binance_acc.get_symbol_info(symbol)

        #calculate the percentage of tickSize for coin relative to coin price
        tick_size_percent = float(symbol_info["filters"][0]["tickSize"])/float(price)
        stoploss_percent = tick_size_percent if tick_size_percent > 0.1 else 0.1
        stoploss_percent = 1 - stoploss_percent

        min_notional_BTC_equivalent = float(symbol_info["filters"][3]["minNotional"])/stoploss_percent
        lot_size_min = float(min_notional_BTC_equivalent)/float(price)
        lot_size_depo = float(lot_size_depo)/float(price)

        min_qty = float(symbol_info["filters"][2]["minQty"])

        lot_size_min = math.ceil(lot_size_min)
        lot_size_depo = math.floor(lot_size_depo)

        if lot_size_min > lot_size_depo:
            lot_size = lot_size_min
        else:
            lot_size = lot_size_depo

        #return lot_size
        return lot_size_min

    #function for placing an order by signals that we got
    def place_an_order(self, pair, pair_min_price, pair_stoploss_price) -> dict:
        #calculate lot size, depends of signals price and symbol restriction
        lot_size = self.calculate_lot_size(pair, str("{:.8f}".format(pair_stoploss_price)))
        self.app.send_message(chat_id = self.channel_id, text = "I have calculated lot size for " + pair +
                                                                ", by price - " + str("{:.8f}".format(pair_stoploss_price)) + ". Lot size is: " + str(lot_size))

        # placing an order
        try:
            order = self.binance_acc.create_order(
                                        symbol = pair,
                                        side = SIDE_BUY,
                                        type = "LIMIT",
                                        timeInForce = TIME_IN_FORCE_GTC,
                                        quantity = lot_size,
                                        price = str("{:.8f}".format(pair_min_price))
                                        )

            self.app.send_message(chat_id = self.channel_id, text = "I have placed an order: " + str(order))
            return order

        except Exception as err:
            self.app.send_message(chat_id=self.channel_id, text="I have a problem with a order, there is a reason: " + str(err))

    #function for checking an order, moving stoploss if price grew
    def check_order(self, order: dict, check_time: int, pair_stoploss_price, pair_min_price, pair_max_price) -> None:
        order_stat = self.binance_acc.get_order(symbol = order["symbol"], orderId = order["orderId"])
        #order_stat = {'symbol': 'POEBTC', 'orderId': 28625410, 'orderListId': -1, 'clientOrderId': 'zua3ZVKgWUUI5OE8UscwPu', 'price': '0.00000012', 'origQty': '1251.00000000', 'executedQty': '1251.00000000', 'cummulativeQuoteQty': '0.00015012', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'BUY', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1588682374773, 'updateTime': 1588682374773, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}

        # loop while order is living, or canceled, or filled, or stoploss is filled
        while True:
            time.sleep(check_time)
            self.app.send_message(chat_id=self.channel_id, text="Check a status of the order")

            # if order isn't filled yet
            if order_stat["status"] == 'NEW' and order_stat["type"] == 'LIMIT':
                time_dif = datetime.now() - datetime.utcfromtimestamp(order_stat["time"]/1000)

                # if an order yonger then 1 days continue
                if time_dif.days < 1:
                    self.app.send_message(chat_id=self.channel_id, text="Order is not fill and it younger than 1 day, continue order checking")
                    continue

                # else canceling an order
                else:
                    self.app.send_message(chat_id=self.channel_id, text="Order is not fill and older than 1 day, cancelling order")
                    result = self.binance_acc.cancel_order(
                                                symbol = order["symbol"],
                                                orderId = order["orderId"]
                                                )
                    self.app.send_message(chat_id=self.channel_id,
                                          text="I have canceled an order: " + str(result))
                    break

            #else if order filled
            elif order_stat["status"] == 'FILLED' and order_stat["type"] == 'LIMIT':
                time_dif = datetime.now() - datetime.utcfromtimestamp(order_stat["time"]/1000)

                # order yonger then 2 days
                if time_dif.days < 2:
                    self.app.send_message(chat_id=self.channel_id,
                                          text="Order filled and it younger than 2 days")

                    OCO_order = self.get_OCO(order_stat)

                    if not OCO_order:
                        self.app.send_message(chat_id=self.channel_id,
                                              text="There is no OCO order, I'm going to make it")
                        try:
                            OCO_order = self.binance_acc.create_oco_order(
                                                                    symbol = order["symbol"],
                                                                    side = SIDE_SELL,
                                                                    quantity = order_stat["executedQty"],
                                                                    price = str("{:.8f}".format(pair_max_price)),
                                                                    stopPrice = str("{:.8f}".format(pair_stoploss_price)),
                                                                    stopLimitPrice = str("{:.8f}".format(pair_stoploss_price)),
                                                                    stopLimitTimeInForce = TIME_IN_FORCE_GTC
                                                                    )

                            self.app.send_message(chat_id=self.channel_id,
                                                  text="I have made an OCO order, here it is: " + str(OCO_order))
                        except Exception as err:
                            self.app.send_message(chat_id=self.channel_id,
                                                  text="I have a problem with a order, there is a reason: " + str(err))

                    # else there is a stoploss checking status, if filled then break loop
                    elif OCO_order["status"] == "FILLED":
                        result = OCO_order
                        self.app.send_message(chat_id=self.channel_id,
                                              text="OCO order filled: " + str(result))
                        break
                    # else if stoploss canceled then break loop
                    elif OCO_order["status"] == "CANCELED":
                        result = OCO_order
                        self.app.send_message(chat_id=self.channel_id,
                                              text="OCO order filled: " + str(result))
                        break
                    else:
                        pass

                # else if order older than 2 days, cancelling stoploss and sell all buy current price
                else:
                    prices = self.binance_acc.get_order_book(symbol=order_stat["symbol"], limit=10)
                    price = float(prices["bids"][0][0])
                    OCO_order = self.get_OCO(order_stat)
                    if OCO_order:
                        self.binance_acc.cancel_order(
                                            symbol = OCO_order["symbol"],
                                            orderId = OCO_order["orderId"]
                                            )
                    result = self.binance_acc.create_order(
                                        symbol=order_stat["symbol"],
                                        side=SIDE_SELL,
                                        type="LIMIT",
                                        timeInForce=TIME_IN_FORCE_GTC,
                                        quantity=order_stat["executedQty"],
                                        price=str("{:.8f}".format(price)),
                                        stopPrice=str("{:.8f}".format(price))
                                        )
                    result = "Order was filled. Order is older than 10 days. Selling coins by current price /n \n" + str(result)
                    return result
            # elif ордер filled но не до конца
                # проверяем возраст ордера, если больше 10 дней, отменяем текущий, выставляем купленное на продажу по текущей цене
                # если меньше
                    #проверяем насколько текущая цена выше цены ордера, если выше на 4 процента и более
                        # отменяем текущий ордер
                        # продаем купленное количество по текущей цене
                    # если ниже 4 процентов продолжаем ходить по циклу
        return result

if __name__ == "__main__":
    acc = "st;StanislavTomilov;+79896117700;655383;" \
                          "88db0805d24311ea0e8f05e2115aa1a2;w2IziKnAei0LOxtvDNrGBeNTuJyYJkWKz5dqE2kFSQ3FAejv7lrxUVDZw8FWfBlu;jc8qXiGprGkFfz5uiQM3QLTi0jQdxXGPmC37rNTsjKQNYeeqLaJ0IacXJVuxnwUS".split(";")

    acc = Account(acc[1], acc[2], acc[3], acc[4], acc[5], acc[6], "test")
    print(acc.calculate_lot_size("NPXSBTC", "0.00000003"))
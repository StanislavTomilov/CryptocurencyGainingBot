from Factory import Account

from binance import client
from pyrogram import Client


#connect to binance
acc = Account(
    name='Tomilov',
    phone_number='+79896117700',
    t_api_id='655383',
    t_api_hash='88db0805d24311ea0e8f05e2115aa1a2',
    b_api_key='4JxbvNI3i2qBzkYA5XgfBqgPMOK8VuBagmgbsy4cP1LEtGJm3aSeiEJE6IQDYJHV',
    b_secret_key='SIGOwlhr4Rbu7FJcC8Vq2RjSoHhtHn5oRC8dF3FYuxdpDCdzx2Xt7wZlKbzvEYda',
    message_text='test',
    channel_id = -1001343025494
)

#pair settings
pair = 'POEBTC'
pair_stoploss_price = 0.00000009
pair_min_price = 0.00000011
pair_max_price = 0.00000012
check_time = 900

#type a pair
#type borders
#type timeframes: checktime

#check status of account: search for opened orders for buy, for sell

order = {
          "symbol":"POEBTC",
          "orderId":28624543,
          "orderListId":-1,
          "clientOrderId":"fuGArz7LjGm9CwbO72a4Cb",
          "price":"0.00000012",
          "origQty":"834.00000000",
          "executedQty":"834.00000000",
          "cummulativeQuoteQty":"0.00010008",
          "status":"FILLED",
          "timeInForce":"GTC",
          "type":"LIMIT",
          "side":"BUY",
          "stopPrice":"0.00000000",
          "icebergQty":"0.00000000",
          "time":1588593209811,
          "updateTime":1588593209811,
          "isWorking":True,
          "origQuoteOrderQty":"0.00000000"
        }
#starting telegram client

while True:
    #set buy order
    order = acc.place_an_order(pair, pair_min_price, pair_stoploss_price)

    #check order
    acc.check_order(order, check_time, pair_stoploss_price, pair_min_price, pair_max_price)

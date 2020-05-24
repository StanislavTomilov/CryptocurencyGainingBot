# from TradingBot import TradingBot
#
# from pyrogram import Client
#
# # TCG API - 1185784482:AAHZKdzkPzS6NTBGsB8Dw4OKAN99USg_xkc
# CGB = TelegramBot()
#
#
# #connect to binance
# acc = TradingBot(
#                     name='Tomilov',
#                     phone_number='+79896117700',
#                     t_api_id='655383',
#                     t_api_hash='88db0805d24311ea0e8f05e2115aa1a2',
#                     b_api_key='4JxbvNI3i2qBzkYA5XgfBqgPMOK8VuBagmgbsy4cP1LEtGJm3aSeiEJE6IQDYJHV',
#                     b_secret_key='SIGOwlhr4Rbu7FJcC8Vq2RjSoHhtHn5oRC8dF3FYuxdpDCdzx2Xt7wZlKbzvEYda',
#                     message_text='test',
#                     channel_id = -1001343025494
#                 )
#
# # Data for connection to Telegram account
# phone_number = '+79896117700'
# api_id = 655383
# api_hash = '88db0805d24311ea0e8f05e2115aa1a2'
#
# # Getting a connection to Telegram account
# app = Client('my-session', phone_number = phone_number, api_id = api_id, api_hash = api_hash)
#
# #pair settings
# pair = 'POEBTC'
# pair_stoploss_price = 0.00000009
# pair_min_price = 0.00000010
# pair_max_price = 0.00000011
# check_time = 900
#
#
#
#
#
#
#
# #check status of account: search for opened orders for buy, for sell
#
# # @app.on_message()
# # def start_app(t_client, message):
# #     pass
#
#
# def play():
#     while True:
#         #set buy order
#         order = acc.place_an_order(pair, pair_min_price, pair_stoploss_price)
#
#         #check order
#         acc.check_order(order, check_time, pair_stoploss_price, pair_min_price, pair_max_price)
#

from Factory import Account
from pyrogram import Client


#connect to binance
acc = Account(
    name='Tomilov',
    phone_number='+79896117700',
    t_api_id='655383',
    t_api_hash='88db0805d24311ea0e8f05e2115aa1a2',
    b_api_key='4JxbvNI3i2qBzkYA5XgfBqgPMOK8VuBagmgbsy4cP1LEtGJm3aSeiEJE6IQDYJHV',
    b_secret_key='SIGOwlhr4Rbu7FJcC8Vq2RjSoHhtHn5oRC8dF3FYuxdpDCdzx2Xt7wZlKbzvEYda',
    message_text='test'
)

# Getting a connection to Telegram account
app = Client('my-session', phone_number = acc.phone_number, api_id = acc.t_api_id, api_hash = acc.t_api_hash)

channel_id = -1001343025494

app.start()
app.send_message(chat_id = channel_id, text = "test")
app.stop()
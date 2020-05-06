from TradingBot import TradingBot

import telebot
from telebot import types

API_TOKEN = '1185784482:AAHZKdzkPzS6NTBGsB8Dw4OKAN99USg_xkc'
TICK_SIZE = 0.00000001
CHECK_TIME = 900

bot = telebot.TeleBot(API_TOKEN)

order_dict = {}
#PAIR_LIST = ['ETHBTC', 'LTCBTC', 'BNBBTC', 'NEOBTC', 'BCCBTC', 'GASBTC', 'HSRBTC', 'MCOBTC', 'WTCBTC', 'LRCBTC', 'QTUMBTC', 'YOYOBTC', 'OMGBTC', 'ZRXBTC', 'STRATBTC', 'SNGLSBTC', 'BQXBTC', 'KNCBTC', 'FUNBTC', 'SNMBTC', 'IOTABTC', 'LINKBTC', 'XVGBTC', 'SALTBTC', 'MDABTC', 'MTLBTC', 'SUBBTC', 'EOSBTC', 'SNTBTC', 'ETCBTC', 'MTHBTC', 'ENGBTC', 'DNTBTC', 'ZECBTC', 'BNTBTC', 'ASTBTC', 'DASHBTC', 'OAXBTC', 'ICNBTC', 'BTGBTC', 'EVXBTC', 'REQBTC', 'VIBBTC', 'TRXBTC', 'POWRBTC', 'ARKBTC', 'XRPBTC', 'MODBTC', 'ENJBTC', 'STORJBTC', 'VENBTC', 'KMDBTC', 'RCNBTC', 'NULSBTC', 'RDNBTC', 'XMRBTC', 'DLTBTC', 'AMBBTC', 'BATBTC', 'BCPTBTC', 'ARNBTC', 'GVTBTC', 'CDTBTC', 'GXSBTC', 'POEBTC', 'QSPBTC', 'BTSBTC', 'XZCBTC', 'LSKBTC', 'TNTBTC', 'FUELBTC', 'MANABTC', 'BCDBTC', 'DGDBTC', 'ADXBTC', 'ADABTC', 'PPTBTC', 'CMTBTC', 'XLMBTC', 'CNDBTC', 'LENDBTC', 'WABIBTC', 'TNBBTC', 'WAVESBTC', 'GTOBTC', 'ICXBTC', 'OSTBTC', 'ELFBTC', 'AIONBTC', 'NEBLBTC', 'BRDBTC', 'EDOBTC', 'WINGSBTC', 'NAVBTC', 'LUNBTC', 'TRIGBTC', 'APPCBTC', 'VIBEBTC', 'RLCBTC', 'INSBTC', 'PIVXBTC', 'IOSTBTC', 'CHATBTC', 'STEEMBTC', 'NANOBTC', 'VIABTC', 'BLZBTC', 'AEBTC', 'RPXBTC', 'NCASHBTC', 'POABTC', 'ZILBTC', 'ONTBTC', 'STORMBTC', 'XEMBTC', 'WANBTC', 'WPRBTC', 'QLCBTC', 'SYSBTC', 'GRSBTC', 'CLOAKBTC', 'GNTBTC', 'LOOMBTC', 'BCNBTC', 'REPBTC', 'TUSDBTC', 'ZENBTC', 'SKYBTC', 'CVCBTC', 'THETABTC', 'IOTXBTC', 'QKCBTC', 'AGIBTC', 'NXSBTC', 'DATABTC', 'SCBTC', 'NPXSBTC', 'KEYBTC', 'NASBTC', 'MFTBTC', 'DENTBTC', 'ARDRBTC', 'HOTBTC', 'VETBTC', 'DOCKBTC', 'POLYBTC', 'PHXBTC', 'HCBTC', 'GOBTC', 'PAXBTC', 'RVNBTC', 'DCRBTC', 'MITHBTC', 'BCHABCBTC', 'BCHSVBTC', 'RENBTC', 'BTTBTC', 'ONGBTC', 'FETBTC', 'CELRBTC', 'MATICBTC', 'ATOMBTC', 'PHBBTC', 'TFUELBTC', 'ONEBTC', 'FTMBTC', 'BTCBBTC', 'ALGOBTC', 'ERDBTC', 'DOGEBTC', 'DUSKBTC', 'ANKRBTC', 'WINBTC', 'COSBTC', 'COCOSBTC', 'TOMOBTC', 'PERLBTC', 'CHZBTC', 'BANDBTC', 'BEAMBTC', 'XTZBTC', 'HBARBTC', 'NKNBTC', 'STXBTC', 'KAVABTC', 'ARPABTC', 'CTXCBTC', 'BCHBTC', 'TROYBTC', 'VITEBTC', 'FTTBTC', 'OGNBTC', 'DREPBTC', 'TCTBTC', 'WRXBTC', 'LTOBTC', 'MBLBTC', 'COTIBTC', 'STPTBTC', 'SOLBTC', 'CTSIBTC', 'HIVEBTC', 'CHRBTC']
PAIR_LIST = ['HOTBTC', 'POEBTC', 'STORMBTC', 'MBLBTC', 'TNBBTC']


class Order:
    def __init__(self, pair):
        self.pair = pair
        self.buy_price = None
        self.sell_price = None
        self.stoploss_price = None


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def welcome(message):
    try:
        bot.reply_to(message, "Hi, I'm a CryptoGainingBot, I'm trying to gain BTC by buying some coin cheaper and selling it pricey.")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('HOTBTC', 'POEBTC', 'STORMBTC', 'MBLBTC', 'TNBBTC')
        #markup.add(PAIR_LIST.__str__()[1,-1])
        # for pair in PAIR_LIST:
        #     markup.add(pair)
        msg = bot.send_message(message.chat.id, "Type a pair for trading, for example 'POEBTC'", reply_markup=markup)
        bot.register_next_step_handler(msg, process_pair_step)
    except Exception as e:
        bot.reply_to(message, 'Some error: ' + e.__str__())


def process_pair_step(message):
    try:
        chat_id = message.chat.id
        pair = message.text
        if not pair in PAIR_LIST:
            msg = bot.reply_to(message, "You entered a wrong pair, please try again, for example 'HOTBTC'")
            bot.register_next_step_handler(msg, process_pair_step())
            return
        order = Order(pair)
        order_dict[chat_id] = order
        msg = bot.reply_to(message, 'Type buy price')
        bot.register_next_step_handler(msg, process_buy_price_step)
    except Exception as e:
        bot.reply_to(message, 'Some error: ' + e.__str__())


def process_buy_price_step(message):
    try:
        chat_id = message.chat.id
        try:
            buy_price = int(message.text)
        except Exception as e:
            msg = bot.reply_to(message, "Price should be a number. Type it again")
            bot.register_next_step_handler(msg, process_buy_price_step)
            return

        if buy_price < 1:
            msg = bot.reply_to(message, 'Price that you have entered is too low')
            bot.register_next_step_handler(msg, process_buy_price_step)
            return

        order = order_dict[chat_id]
        order.buy_price = buy_price * TICK_SIZE
        msg = bot.send_message(message.chat.id, 'Type sell price')
        bot.register_next_step_handler(msg, process_sell_price_step)
    except Exception as e:
        bot.reply_to(message, 'Some error: ' + e.__str__())


def process_sell_price_step(message):
    try:
        chat_id = message.chat.id
        try:
            sell_price = int(message.text)
        except Exception as e:
            msg = bot.reply_to(message, "Price should be a number. Type it again")
            bot.register_next_step_handler(msg, process_buy_price_step)
            return

        if sell_price < 1:
            msg = bot.reply_to(message, 'Price that you have entered is too low')
            bot.register_next_step_handler(msg, process_buy_price_step)
            return

        order = order_dict[chat_id]
        order.sell_price = sell_price * TICK_SIZE
        msg = bot.send_message(message.chat.id, 'Type stoploss price')
        bot.register_next_step_handler(msg, process_stoploss_price_step)
    except Exception as e:
        bot.reply_to(message, 'Some error: ' + e.__str__())


def process_stoploss_price_step(message):
    try:
        chat_id = message.chat.id
        try:
            stoploss_price = int(message.text)
        except Exception as e:
            msg = bot.reply_to(message, "Price should be a number. Type it again")
            bot.register_next_step_handler(msg, process_buy_price_step)
            return

        if stoploss_price < 1:
            msg = bot.reply_to(message, 'Price that you have entered is too low')
            bot.register_next_step_handler(msg, process_buy_price_step)
            return

        order = order_dict[chat_id]
        order.stoploss_price = stoploss_price * TICK_SIZE
        bot.send_message(message.chat.id, "There is a parametrs that I'm going to use for gaining BTC:")
        bot.send_message(message.chat.id, "I'm going to traid " + order.pair + " pair.")
        bot.send_message(message.chat.id, "I'm going to buy at a " + str("{:.8f}".format(order.buy_price)) + " price.")
        bot.send_message(message.chat.id, "I'm going to sell at a " + str("{:.8f}".format(order.sell_price)) + " price.")
        bot.send_message(message.chat.id, "I'm going to make a stoploss order for " + str("{:.8f}".format(order.stoploss_price))
                         + " price.")

        markup = types.ReplyKeyboardMarkup()
        markup.add("START", "RESET")
        msg = bot.send_message(chat_id, "Let's go?", reply_markup=markup)
        bot.register_next_step_handler(msg, process_total_step)
    except Exception as e:
        bot.reply_to(message, 'Some error: ' + e.__str__())


def process_total_step(message):
    try:
        chat_id = message.chat.id
        order = order_dict[chat_id]
        next_step = message.text

        if next_step == "START":
            bot.reply_to(message, "Start working:")

            acc = TradingBot(
                                name='Tomilov',
                                phone_number='+79896117700',
                                t_api_id='655383',
                                t_api_hash='88db0805d24311ea0e8f05e2115aa1a2',
                                b_api_key='4JxbvNI3i2qBzkYA5XgfBqgPMOK8VuBagmgbsy4cP1LEtGJm3aSeiEJE6IQDYJHV',
                                b_secret_key='SIGOwlhr4Rbu7FJcC8Vq2RjSoHhtHn5oRC8dF3FYuxdpDCdzx2Xt7wZlKbzvEYda',
                                message_text='test',
                                telegram_bot=bot,
                                chat_id = chat_id
                            )

            while True:
                # set buy order
                binance_order = acc.place_an_order(order.pair, order.buy_price, order.stoploss_price)

                # check order
                acc.check_order(binance_order, CHECK_TIME, order.stoploss_price, order.buy_price, order.sell_price)
        else:
            bot.reply_to((message, "Ok, type '/start' to try again"))
            return
    except Exception as e:
        bot.send_message(chat_id, "Some error: " + e.__str__())



# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling()
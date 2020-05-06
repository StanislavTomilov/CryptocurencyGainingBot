
# -*- coding: utf-8 -*-
"""
This Example will show you how to use register_next_step handler.
"""

import telebot
from telebot import types

API_TOKEN = '<api_token>'

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Hi there, I am Example bot.
What's your name?
""")
    bot.register_next_step_handler(msg, process_name_step)


def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'How old are you?')
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, 'Age should be a number. How old are you?')
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Male', 'Female')
        msg = bot.reply_to(message, 'What is your gender', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_sex_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == u'Male') or (sex == u'Female'):
            user.sex = sex
        else:
            raise Exception()
        bot.send_message(chat_id, 'Nice to meet you ' + user.name + '\n Age:' + str(user.age) + '\n Sex:' + user.sex)
    except Exception as e:
        bot.reply_to(message, 'oooops')


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling()




# from binance import client
# from binance.enums import *
# from pyrogram import Client


#client.Client('4JxbvNI3i2qBzkYA5XgfBqgPMOK8VuBagmgbsy4cP1LEtGJm3aSeiEJE6IQDYJHV', 'SIGOwlhr4Rbu7FJcC8Vq2RjSoHhtHn5oRC8dF3FYuxdpDCdzx2Xt7wZlKbzvEYda

# import telebot
# from telebot import types
#
# API_TOKEN = '1185784482:AAHZKdzkPzS6NTBGsB8Dw4OKAN99USg_xkc'
#
# bot = telebot.TeleBot(API_TOKEN)
#
# user_dict = {}
#
#
# class User:
#     def __init__(self, name):
#         self.name = name
#         self.age = None
#         self.sex = None
#
#
# # Handle '/start' and '/help'
# @bot.message_handler(commands=['help', 'start'])
# def send_welcome(message):
#     msg = bot.reply_to(message, """\
# Hi there, I am Example bot.
# What's your name?
# """)
#     bot.register_next_step_handler(msg, process_name_step)
#
#
# def process_name_step(message):
#     try:
#         chat_id = message.chat.id
#         name = message.text
#         user = User(name)
#         user_dict[chat_id] = user
#         msg = bot.reply_to(message, 'How old are you?')
#         bot.register_next_step_handler(msg, process_age_step)
#     except Exception as e:
#         bot.reply_to(message, 'oooops')
#
#
# def process_age_step(message):
#     try:
#         chat_id = message.chat.id
#         age = message.text
#         if not age.isdigit():
#             msg = bot.reply_to(message, 'Age should be a number. How old are you?')
#             bot.register_next_step_handler(msg, process_age_step)
#             return
#         user = user_dict[chat_id]
#         user.age = age
#         markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
#         markup.add('Male', 'Female')
#         msg = bot.reply_to(message, 'What is your gender', reply_markup=markup)
#         bot.register_next_step_handler(msg, process_sex_step)
#     except Exception as e:
#         bot.reply_to(message, 'oooops')
#
#
# def process_sex_step(message):
#     try:
#         chat_id = message.chat.id
#         sex = message.text
#         user = user_dict[chat_id]
#         if (sex == 'Male') or (sex == 'Female'):
#             user.sex = sex
#         else:
#             raise Exception()
#         bot.send_message(chat_id, 'Nice to meet you ' + user.name + '\n Age:' + str(user.age) + '\n Sex:' + user.sex)
#     except Exception as e:
#         bot.reply_to(message, 'oooops')
#
#
# # Enable saving next step handlers to file "./.handlers-saves/step.save".
# # Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# # saving will hapen after delay 2 seconds.
# bot.enable_save_next_step_handlers(delay=2)
#
# # Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# # WARNING It will work only if enable_save_next_step_handlers was called!
# bot.load_next_step_handlers()
#
# bot.polling()


# import telebot
#
# bot = telebot.TeleBot("1185784482:AAHZKdzkPzS6NTBGsB8Dw4OKAN99USg_xkc")
#
# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
# 	bot.reply_to(message, "Howdy, how are you doing?")
#
# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
# 	bot.reply_to(message, message.text)
#
# bot.polling()

# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # This program is dedicated to the public domain under the CC0 license.
#
# """
# First, a few callback functions are defined. Then, those functions are passed to
# the Dispatcher and registered at their respective places.
# Then, the bot is started and runs until we press Ctrl-C on the command line.
# Usage:
# Example of a bot-user conversation using ConversationHandler.
# Send /start to initiate the conversation.
# Press Ctrl-C on the command line or send a signal to the process to stop the
# bot.
# """
#
# import logging
#
# from telegram import ReplyKeyboardMarkup
# from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
#                           ConversationHandler)
#
# # Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)
#
# logger = logging.getLogger(__name__)
#
# CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)
#
# reply_keyboard = [['Age', 'Favourite colour'],
#                   ['Number of siblings', 'Something else...'],
#                   ['Done']]
# markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
#
#
# def facts_to_str(user_data):
#     facts = list()
#
#     for key, value in user_data.items():
#         facts.append('{} - {}'.format(key, value))
#
#     return "\n".join(facts).join(['\n', '\n'])
#
#
# def start(update, context):
#     update.message.reply_text(
#         "Hi! My name is Doctor Botter. I will hold a more complex conversation with you. "
#         "Why don't you tell me something about yourself?",
#         reply_markup=markup)
#
#     return CHOOSING
#
#
# def regular_choice(update, context):
#     text = update.message.text
#     context.user_data['choice'] = text
#     update.message.reply_text(
#         'Your {}? Yes, I would love to hear about that!'.format(text.lower()))
#
#     return TYPING_REPLY
#
#
# def custom_choice(update, context):
#     update.message.reply_text('Alright, please send me the category first, '
#                               'for example "Most impressive skill"')
#
#     return TYPING_CHOICE
#
#
# def received_information(update, context):
#     user_data = context.user_data
#     text = update.message.text
#     category = user_data['choice']
#     user_data[category] = text
#     del user_data['choice']
#
#     update.message.reply_text("Neat! Just so you know, this is what you already told me:"
#                               "{} You can tell me more, or change your opinion"
#                               " on something.".format(facts_to_str(user_data)),
#                               reply_markup=markup)
#
#     return CHOOSING
#
#
# def done(update, context):
#     user_data = context.user_data
#     if 'choice' in user_data:
#         del user_data['choice']
#
#     update.message.reply_text("I learned these facts about you:"
#                               "{}"
#                               "Until next time!".format(facts_to_str(user_data)))
#
#     user_data.clear()
#     return ConversationHandler.END
#
#
# def error(update, context):
#     """Log Errors caused by Updates."""
#     logger.warning('Update "%s" caused error "%s"', update, context.error)
#
#
# def main():
#     # Create the Updater and pass it your bot's token.
#     # Make sure to set use_context=True to use the new context based callbacks
#     # Post version 12 this will no longer be necessary
#     updater = Updater("1185784482:AAHZKdzkPzS6NTBGsB8Dw4OKAN99USg_xkc", use_context=True)
#
#     # Get the dispatcher to register handlers
#     dp = updater.dispatcher
#
#     # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler('start', start)],
#
#         states={
#             CHOOSING: [MessageHandler(Filters.regex('^(Age|Favourite colour|Number of siblings)$'),
#                                       regular_choice),
#                        MessageHandler(Filters.regex('^Something else...$'),
#                                       custom_choice)
#                        ],
#
#             TYPING_CHOICE: [MessageHandler(Filters.text,
#                                            regular_choice)
#                             ],
#
#             TYPING_REPLY: [MessageHandler(Filters.text,
#                                           received_information),
#                            ],
#         },
#
#         fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
#     )
#
#     dp.add_handler(conv_handler)
#
#     # log all errors
#     dp.add_error_handler(error)
#
#     # Start the Bot
#     updater.start_polling()
#
#     # Run the bot until you press Ctrl-C or the process receives SIGINT,
#     # SIGTERM or SIGABRT. This should be used most of the time, since
#     # start_polling() is non-blocking and will stop the bot gracefully.
#     updater.idle()
#
#
# if __name__ == '__main__':
#     main()


# from telegram.ext import Updater
# import logging
# from telegram.ext import CommandHandler
# from telegram.ext import MessageHandler, Filters
# from telegram import InlineQueryResultArticle, InputTextMessageContent
#
#
# from telegram.ext import InlineQueryHandler
#
# updater = Updater(token='1185784482:AAHZKdzkPzS6NTBGsB8Dw4OKAN99USg_xkc', use_context=True)
# dispatcher = updater.dispatcher
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
#
# def start(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
#
# start_handler = CommandHandler('start', start)
# dispatcher.add_handler(start_handler)
#
# updater.start_polling()
#
# def stop(update, context):
#     pass
#
#
# def echo(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
#
#
# echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
# dispatcher.add_handler(echo_handler)
#
# def caps(update, context):
#     text_caps = ' '.join(context.args).upper()
#     context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
#
# caps_handler = CommandHandler('caps', caps)
# dispatcher.add_handler(caps_handler)
#
# def inline_caps(update, context):
#     query = update.inline_query.query
#     if not query:
#         return
#     results = list()
#     results.append(
#         InlineQueryResultArticle(
#             id=query.upper(),
#             title='Caps',
#             input_message_content=InputTextMessageContent(query.upper())
#         )
#     )
#     context.bot.answer_inline_query(update.inline_query.id, results)
#
# inline_caps_handler = InlineQueryHandler(inline_caps)
# dispatcher.add_handler(inline_caps_handler)
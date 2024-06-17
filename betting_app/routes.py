import numpy as np
import re
import os
import configparser
import asyncio
from typing import Final
import requests
from flask import Flask, request
from flask import current_app as app
from flask import jsonify
import telegram
from telegram import BotCommand
from telegram.ext import Updater, CommandHandler, Dispatcher

from .utils import read_config
from .models import Database

config = read_config()

global TOKEN
global USERNAME
global URL
TOKEN: Final = config['TELEGRAM']['TOKEN']
USERNAME: Final = config['TELEGRAM']['BOT_USERNAME']
URL: Final = config['TELEGRAM']['URL']

data = Database('data.db', 'sample_data.csv')

global BOT
BOT = telegram.Bot(token=TOKEN)
dispatcher = Dispatcher(BOT, None, use_context=True)

async def send_message(chat_id, msg_id, msg):
    await BOT.sendMessage(chat_id=chat_id, text=msg, reply_to_message_id=msg_id)

def start_command(update, context):
    update.message.reply_text('Hello! I am your bot. Use /help to see available commands.')

def help_command(update, context):
    update.message.reply_text('These are the available commands:\n/start - Start the bot\n/help - Get help')


# Register handlers
dispatcher.add_handler(CommandHandler("start", start_command))
dispatcher.add_handler(CommandHandler("help", help_command))

# Set bot commands
commands = [
    BotCommand("start", "Start the bot"),
    BotCommand("help", "Get help")
]
BOT.bot.set_my_commands(commands)

@app.route('/')
def index():
    print('ok')
    return 'test'

@app.route('/test', methods=['GET'])
def test():
    print('ok')
    return 'test'

@app.route('/set_webhook', methods=['GET','POST'])
def set_webhook():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(async_set_webhook())
        return "Webhook set successfully!"
    except Exception as e:
        return f"Failed to set webhook: {e}"

async def async_set_webhook():
    
    await BOT.setWebhook(url='{URL}/test_webhook'.format(URL=URL))

@app.route('/test_webhook', methods=['GET','POST'])
def test_webhook():
    
    if request.method == 'POST':
        update = telegram.Update.de_json(request.get_json(force=True), BOT)
        #dispatcher.process_update(update)

        chat_id = update.message.chat.id
        msg_id = update.message.message_id

        text = update.message.text.encode('utf-8').decode()
        print("got text message :", text)

        if text == "/test":
            bot_welcome = """
                This is Luca's Sports Betting App...
                """
            #await BOT.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
            loop_send_msg = asyncio.new_event_loop()
            asyncio.set_event_loop(loop_send_msg)
            loop_send_msg.run_until_complete(send_message(chat_id, msg_id, bot_welcome))

        elif text == '/name':
            query = data.fetch_name_data('Raghav Jaisinghani')

            #await BOT.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
            loop_send_msg = asyncio.new_event_loop()
            asyncio.set_event_loop(loop_send_msg)
            loop_send_msg.run_until_complete(send_message(chat_id, msg_id, query['aces'].to_string()))

        return 'msg'

    return 'ok'


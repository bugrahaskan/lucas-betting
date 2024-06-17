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
from telegram import BotCommand, Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, Updater

from .utils import read_config, extract_args
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
update = telegram.Update.de_json(request.get_json(force=True), BOT)
updater = Updater(bot=BOT, update_queue=update)
updater.start_webhook()

async def async_set_webhook():
    await BOT.setWebhook(url='{URL}/webhook'.format(URL=URL))

async def send_message(chat_id, msg_id, msg):
    await BOT.sendMessage(chat_id=chat_id, text=msg, reply_to_message_id=msg_id)

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

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    
    if request.method == 'POST':
        #update = telegram.Update.de_json(request.get_json(force=True), BOT)

        chat_id = update.message.chat.id
        msg_id = update.message.message_id

        text = update.message.text.encode('utf-8').decode()
        print("got text message :", text)

        if text == "/start":
            bot_welcome = """
                This is Luca's Sports Betting App...
                """
            
            loop_send_msg = asyncio.new_event_loop()
            asyncio.set_event_loop(loop_send_msg)
            loop_send_msg.run_until_complete(send_message(chat_id, msg_id, bot_welcome))

        elif text.startswith('/name'):
            #player1, player2 = extract_args('/name', text)
            # more here

            query = data.fetch_name_data('Raghav Jaisinghani')

            loop_send_msg = asyncio.new_event_loop()
            asyncio.set_event_loop(loop_send_msg)
            loop_send_msg.run_until_complete(send_message(chat_id, msg_id, query['aces'].to_string()))

        
        return 'msg'

    return 'ok'


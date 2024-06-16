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

from .utils import read_config

config = read_config()

global TOKEN
global USERNAME
global URL
TOKEN: Final = config['TELEGRAM']['TOKEN']
USERNAME: Final = config['TELEGRAM']['BOT_USERNAME']
URL: Final = config['TELEGRAM']['URL']

global BOT
BOT = telegram.Bot(token=TOKEN)

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

        chat_id = update.message.chat.id
        msg_id = update.message.message_id

        text = update.message.text.encode('utf-8').decode()
        print("got text message :", text)

        if text == "/start":
            bot_welcome = """
                This is Luca's Sports Betting App...
                """
            BOT.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

        return 'msg'

    return 'ok'

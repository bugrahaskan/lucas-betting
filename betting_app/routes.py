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

@app.route('/set_webhook', methods=['GET', 'POST'])
async def async_set_webhook():
    s = await BOT.setWebhook(url='{URL}/test_webhook'.format(URL=URL))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/test_webhook', methods=['GET','POST'])
def test():

    return 'test webhook'
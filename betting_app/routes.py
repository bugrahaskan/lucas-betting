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
from queue import Queue
import threading

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
#BOT = telegram.Bot(token=TOKEN)
#application = Application.builder().token(TOKEN).build()
#asyncio.run(Application.initialize(application))
#asyncio.run(Bot.initialize(BOT))

# Define your command handlers
def start(update: Update, context: ContextTypes):
    update.message.reply_text('Hello! I am your bot. How can I help you today?')

def help_command(update: Update, context: ContextTypes):
    update.message.reply_text('Help!')

def echo(update: Update, context: ContextTypes):
    update.message.reply_text(update.message.text)

async def set_commands(application):
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Get help"),
        BotCommand("echo", "Echo me")
    ]
    
    await application.bot.set_my_commands(commands)

async def main():
    # Updater from Telegram API
    update_queue = Queue()
    #updater = Updater(bot=TOKEN, update_queue=update_queue)
    application = Application.builder().token(TOKEN).update_queue(update_queue).build()

    # Add handlers for different commands and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("echo", echo))

    # Set bot commands
    await set_commands(application)
    
    # Start the Bot with polling
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.stop()
    await application.shutdown()

    return application


#def run_telegram_bot():
#    asyncio.run(main())

#bot_thread = threading.Thread(target=run_telegram_bot)
#bot_thread.start()

application = asyncio.run(main())

@app.route('/')
def index():
    print('ok')
    return 'test'

@app.route('/test', methods=['GET'])
def test():
    print('ok')
    return 'test'

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        update = Update.de_json(request.get_json(force=True), application.bot)
        #application.update_queue.put(update)
        asyncio.create_task(application.update.update_queue.put(update))
        return 'ok'

async def async_set_webhook():
    await application.bot.setWebhook(url='{URL}/webhook'.format(URL=URL))

@app.route('/set_webhook', methods=['GET','POST'])
def set_webhook():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(async_set_webhook())
        return "Webhook set successfully!"
    except Exception as e:
        return f"Failed to set webhook: {e}"
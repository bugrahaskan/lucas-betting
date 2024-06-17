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
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

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

# Replace 'YOUR_TOKEN' with your actual bot token
updater = Updater(TOKEN)

dispatcher = updater.dispatcher

# Add handlers for different commands and messages
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(CommandHandler("echo", echo))

# Start the Bot with polling
updater.start_polling()

# Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
updater.idle()
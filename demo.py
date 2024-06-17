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
from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler

from betting_app.utils import read_config, extract_args
from betting_app.models import Database

config = read_config()

global TOKEN
global USERNAME
global URL
TOKEN: Final = config['TELEGRAM']['TOKEN']
USERNAME: Final = config['TELEGRAM']['BOT_USERNAME']
URL: Final = config['TELEGRAM']['URL']

data = Database('data.db', 'sample_data.csv')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('hello')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('help')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('custom command')

def handle_response(text: str):
    processed: str = text.lower()

    if 'hello' in processed:
        return 'hi'
    
    # more

    return "i don't understand the command"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'user ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if USERNAME in text:
            new_text: str = text.replace(USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
        
    else:
        response: str = handle_response(text)

    print('bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update {update} caused error {context.error}')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    app.run_polling(poll_interval=3)
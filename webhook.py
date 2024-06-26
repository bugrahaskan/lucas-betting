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

from betting_app.utils import read_config, extract_args
from betting_app.models import Database

app = Flask(__name__)

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
application = Application.builder().token(TOKEN).build()
asyncio.run(Application.initialize(application))
#asyncio.run(Bot.initialize(BOT))

async def async_set_webhook():
    await BOT.setWebhook(url='{URL}/webhook'.format(URL=URL))

async def send_message(chat_id, msg_id, msg):
    await BOT.sendMessage(chat_id=chat_id, text=msg, reply_to_message_id=msg_id)

#async def start_command(update, context):
#    #await update.message.reply_text('Hello! I am your bot. Use /help to see available commands.')
#    print('start_command')
#    await asyncio.sleep(1)

#async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    print('help_command')
#    await update.message.reply_text('These are the available commands:\n/start - Start the bot\n/help - Get help')
#    #print('help_command')
#    #await asyncio.sleep(1)

async def help_command(update: Update):
    #msg = context.args[0]
    #print(msg)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    #await BOT.send_message(chat_id=chat_id, text='These are the available commands:\n/start - Start the bot\n/help - Get help')
    #await context.bot.send_message(chat_id=chat_id, text='These are the available commands:\n/start - Start the bot\n/help - Get help')
    await BOT.sendMessage(chat_id=chat_id, text='These are the available commands:\n/start - Start the bot\n/help - Get help', reply_to_message_id=msg_id)

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
        update = Update.de_json(request.get_json(force=True), BOT)

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

        if text == '/help':
            loop_send_msg = asyncio.new_event_loop()
            asyncio.set_event_loop(loop_send_msg)
            loop_send_msg.run_until_complete(help_command(update=update))

        if text.startswith('/name'):
            player1, player2 = extract_args('/name', text)
            # more here
            print(player1, player2)

            query = data.fetch_name_data('Raghav Jaisinghani')

            loop_send_msg = asyncio.new_event_loop()
            asyncio.set_event_loop(loop_send_msg)
            loop_send_msg.run_until_complete(send_message(chat_id, msg_id, query['aces'].to_string()))

        
        return 'msg'

    return 'ok'

if __name__ == '__main__':
    # Register handlers
    #application.add_handler(CommandHandler("start", send_message))
    #application.add_handler(CommandHandler("help", help_command))
    #application.add_handler(CommandHandler("name", send_message))

    # Set bot commands
    #commands = [
    #    BotCommand("start", "Start the bot"),
    #    BotCommand("help", "Get help"),
    #    BotCommand("name", "Give name")
    #]

    #async def set_commands(commands):
    #    await application.bot.set_my_commands(commands)

    #loop_set_command = asyncio.new_event_loop()
    #asyncio.set_event_loop(loop_set_command)
    #loop_set_command.run_until_complete(set_commands(commands))

    app.run(host=config['SETTINGS']['HOST'],
            port=config['SETTINGS']['PORT'],
            threaded=config['SETTINGS']['THREADED'],
            debug=config['SETTINGS']['DEBUG'],
            #ssl_context=('cert.pem', 'key.pem'))
            #ssl_context=('nginx-selfsigned.crt', 'nginx-selfsigned.key')
            )
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

#@app.route('/set_webhook', methods=['GET', 'POST'])
async def async_set_webhook():
    cert_path = os.getcwd()+'/nginx-selfsigned.crt'
    if os.path.exists(cert_path) and os.path.isfile(cert_path):
        print("Certificate file exists and is accessible.")
        print(os.getcwd()+'/cert.pem')
        await BOT.setWebhook(url='{URL}/test'.format(URL=URL))
    else:
        print('certificate not read')
    #s = await BOT.setWebhook(url='{URL}/test'.format(URL=URL), certificate=telegram.InputFile('../cert.pem'))
    #if s:
    #    return "webhook setup ok"
    #else:
    #    return "webhook setup failed"

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method == 'POST':
        update = request.json  # Retrieve the JSON data sent by Telegram
        print(update)  # Print the update to see what Telegram sends
        # Add your logic to process the update and generate a response

        # Example response (echo back the received message)
        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            text = message.get('text', '')

            # Respond with the same message
            response_text = f"You said: {text}"
            send_message(chat_id, response_text)  # Example function to send a message

        return jsonify({'status': 'ok'})

    return '', 200  # Respond with an empty body and HTTP status code 200 for other requests

def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, json=payload)
    print(response.json())  # Print the response from Telegram API for debugging








@app.route('/test', methods=['GET','POST'])
def test():
    
    if request.method == 'POST':
        update = telegram.Update.de_json(request.get_json(force=True), BOT)

        chat_id = update.message.chat.id
        msg_id = update.message.message_id

        text = update.message.text.encode('utf-8').decode()
        print("got text message :", text)

        return 'msg'

    return 'ok'





'''example:'''
@app.route('/respond', methods=['GET','POST'])
def respond():
   # retrieve the message in JSON and then transform it to Telegram object
   update = telegram.Update.de_json(request.get_json(force=True), BOT)

   chat_id = update.message.chat.id
   msg_id = update.message.message_id

   # Telegram understands UTF-8, so encode text for unicode compatibility
   text = update.message.text.encode('utf-8').decode()
   # for debugging purposes only
   print("got text message :", text)
   # the first time you chat with the bot AKA the welcoming message
   if text == "/start":
       # print the welcoming message
       bot_welcome = """
       Welcome to coolAvatar bot, the bot is using the service from http://avatars.adorable.io/ to generate cool looking avatars based on the name you enter so please enter a name and the bot will reply with an avatar for your name.
       """
       # send the welcoming message
       BOT.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)


   else:
       try:
           # clear the message we got from any non alphabets
           text = re.sub(r"\W", "_", text)
           # create the api link for the avatar based on http://avatars.adorable.io/
           url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
           # reply with a photo to the name the user sent,
           # note that you can send photos by url and telegram will fetch it for you
           BOT.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
       except Exception:
           # if things went wrong
           BOT.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)

   return 'ok'
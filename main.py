import telebot
from telebot import types
import requests
import time

API_TOKEN = '8177256403:AAEOUctn6EhgLjPZQAz7SbprsNPS5uwToUI'
bot = telebot.TeleBot(API_TOKEN)
  #made by @DEVSNP
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=' Generate Random meme', callback_data='generate_random_meme'))

    api_response = requests.get("https://nepcoder.apinepdev.workers.dev/random-meme").json()
    img_url = api_response['url']
  #made by @DEVSNP
    caption_text = "🧑‍💻Developer: @myserver23(my server)"
    bot.send_photo(chat_id='@MYSERVER23', photo=img_url, caption=caption_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'generate_random_meme':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text=' Generate Random meme', callback_data='generate_random_meme'))
  #made by @DEVSNP
        api_response = requests.get("https://nepcoder.apinepdev.workers.dev/random-meme").json()
        img_url = api_response['url']
  #made by @DEVSNP
        media = types.InputMediaPhoto(media=img_url)
        caption_text = "🧑‍💻 Developer: @MYSERVER23(my server)"
        
        time.sleep(1)  #made by @DEVSNP
  #made by @DEVSNP
        try:
            bot.edit_message_media(chat_id=call.message.chat.id, media=media, message_id=call.message.message_id, reply_markup=markup)
            bot.edit_message_caption(chat_id=call.message.chat.id, caption=caption_text, message_id=call.message.message_id, reply_markup=markup)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Telegram API Error: {e}")

bot.polling()

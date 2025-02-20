from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import requests
from bs4 import BeautifulSoup
import re

TOKEN = "8006450488:AAGYArupkfe80eWd0zZvluNJZa0qZp_q5Ws"
AFFILIATE_TAG = "beautyinside4-21"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Send me an Amazon product link, and I'll convert it to an affiliate link.")

# Function to add affiliate tag to Amazon URLs
def add_affiliate_tag(url):
    if "amazon" in url:
        # Use regex to append/update the affiliate tag
        if "tag=" in url:
            url = re.sub(r'tag=.*?(&|$)', f'tag={AFFILIATE_TAG}', url)
        else:
            separator = "&" if "?" in url else "?"
            url += f"{separator}tag={AFFILIATE_TAG}"
        return url
    return None

# Handle incoming messages
def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    affiliate_url = add_affiliate_tag(text)
    
    if affiliate_url:
        update.message.reply_text(f"Affiliate Link:\n{affiliate_url}")
    else:
        update.message.reply_text("Please send a valid Amazon product URL.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(filters.text & ~filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from gtts import gTTS
from langdetect import detect, LangDetectException

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

USER_LANGUAGES = {}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "🌟 Welcome to Universal TTS Bot!\n\n"
        "I can convert text to speech in ANY language!\n\n"
        "• Just send me text\n"
        "• Use /lang [code] to set language (e.g. /lang fr)\n"
        "• Use /help for assistance"
    )

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "📚 Help Center:\n\n"
        "1. Send text → Auto-detect language\n"
        "2. /lang [code] → Set preferred language\n"
        "3. /help → Show this message\n\n"
        "Examples:\n"
        "/lang ru → Russian\n"
        "/lang ar → Arabic\n"
        "/lang hi → Hindi\n\n"
        "Supports 100+ languages!"
    )

def set_language(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    args = context.args

    if not args:
        update.message.reply_text("🔍 Please provide a language code (e.g. /lang de)")
        return

    lang_code = args[0].lower()
    USER_LANGUAGES[user_id] = lang_code
    update.message.reply_text(f"🌍 Language set to: {lang_code.upper()}")

def generate_speech(text: str, lang: str) -> str:
    tts = gTTS(text=text, lang=lang)
    filename = f"tts_{lang}.mp3"
    tts.save(filename)
    return filename

def handle_text(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    text = update.message.text

    try:
        lang = USER_LANGUAGES.get(user_id)
        
        if not lang:
            try:
                lang = detect(text)
            except LangDetectException:
                lang = 'en'

        audio_file = generate_speech(text, lang)
        
        with open(audio_file, "rb") as f:
            update.message.reply_voice(voice=f)
        
        os.remove(audio_file)

    except Exception as e:
        logger.error(f"Error: {e}")
        update.message.reply_text("❌ Error processing your request. Please try again.")

def main() -> None:
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        raise ValueError("Missing TELEGRAM_BOT_TOKEN environment variable")

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("lang", set_language))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    logger.info("Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

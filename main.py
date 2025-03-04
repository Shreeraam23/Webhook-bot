from telethon import TelegramClient, events
import base64
import logging
from datetime import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

API_ID = 20373203
API_HASH = "8962717c7c708e210f66ea658db58d85"
BOT_TOKEN = "7531731133:AAF876StbZbRQxmP9T-H_Yhdy0kXf9tRjAQ" #Enter Your Token
ADMIN_ID = 7369976226 # Replace With Your Id
DB_CHANNEL = -1002380048510 #Replace With Your Channel Id
XOR_KEY = 50 # Don't Use Higher Than 99 

CREATOR = "@myserver23"
START_TIME = datetime.now()

bot = TelegramClient('file_store_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

user_states = {}

def xor(message: str, key: int) -> str:
    return ''.join(chr(ord(m) ^ key) for m in message)

@bot.on(events.NewMessage(pattern='^/start( .+)?$'))
async def start_handler(event):
    try:
        command = event.message.text.split()
        if len(command) > 1:
            encoded_data = command[1]
            try:
                decoded_bytes = base64.b64decode(encoded_data.encode('utf-8'))
                decrypted_data = xor(decoded_bytes.decode('utf-8'), XOR_KEY)
                logger.info(f"Decrypted data: {decrypted_data}")
                try:
                    message_id = int(decrypted_data)
                    message = await bot.get_messages(DB_CHANNEL, ids=message_id)
                    if message:
                        await bot.forward_messages(event.chat_id, message, silent=True)
                    else:
                        await event.respond("Sorry, this message is no longer available.")
                except ValueError:
                    await event.respond("Invalid link format.")
            except Exception as e:
                logger.error(f"Error processing link: {e}")
                await event.respond("Sorry, this link appears to be invalid or expired.")
        else:
            welcome_text = (
                "👋 **Welcome to Message Store Bot!**\n\n"
                "This bot helps you store and share messages securely.\n"
                "Use /gen to generate a new message link (Admin only).\n"
                "Use /status to check bot status."
            )
            await event.respond(welcome_text, parse_mode='markdown')
    except Exception as e:
        logger.error(f"Error in start handler: {e}")
        await event.respond("An error occurred. Please try again later.")

@bot.on(events.NewMessage(pattern='/gen'))
async def gen_handler(event):
    try:
        if event.sender_id != ADMIN_ID:
            await event.respond("Sorry, only admin can use this command.")
            return
        user_states[event.sender_id] = True
        await event.respond("📝 Send any message to generate its link.")
    except Exception as e:
        logger.error(f"Error in gen handler: {e}")
        await event.respond("An error occurred. Please try again later.")

@bot.on(events.NewMessage)
async def message_handler(event):
    try:
        if event.message.text and event.message.text.startswith('/'):
            return
        if event.sender_id != ADMIN_ID or event.sender_id not in user_states:
            return
        del user_states[event.sender_id]
        forwarded_msg = await bot.forward_messages(DB_CHANNEL, event.message, silent=True)
        message_id = str(forwarded_msg.id)
        logger.info(f"Generated message ID: {message_id}")
        encrypted_data = xor(message_id, XOR_KEY)
        encoded_data = base64.b64encode(encrypted_data.encode('utf-8')).decode('utf-8')
        bot_username = (await bot.get_me()).username
        bot_link = f"https://t.me/{bot_username}?start={encoded_data}"
        logger.info(f"Bot link: {bot_link}")
        response_text = (
            "✅ **Message Stored!**\n\n"
            f"🔒 **Bot Link:**\n`{bot_link}`"
        )
        await event.respond(response_text, parse_mode='markdown')
    except Exception as e:
        logger.error(f"Error in message handler: {e}")
        await event.respond("An error occurred while processing your message.")
        if event.sender_id in user_states:
            del user_states[event.sender_id]

@bot.on(events.NewMessage(pattern='/status'))
async def status_handler(event):
    if event.sender_id != ADMIN_ID:
        return
    current_time = datetime.now()
    uptime = current_time - START_TIME
    status_text = (
        "🤖 **Bot Status**\n\n"
        f"👤 Owner: {CREATOR}\n"
        f"⏰ Start Time: {START_TIME.strftime('%Y-%m-%d %H:%M:%S')} UTC\n"
        f"🕒 Current Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')} UTC\n"
        f"⌛️ Uptime: {str(uptime).split('.')[0]}\n"
        "✅ Bot is running normally"
    )
    await event.respond(status_text, parse_mode='markdown')

def main():
    try:
        print("🤖 Message Store Bot")
        print(f"👤 Owner: {CREATOR}")
        print(f"⏰ Time: {START_TIME.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        logger.info("Bot started successfully!")
        bot.run_until_disconnected()
    except Exception as e:
        logger.error(f"Error running bot: {e}")

if __name__ == '__main__':
    main()

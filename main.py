import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

# MADE BY NEPCODER @DEVSNP
bot = telebot.TeleBot('7654906615:AAEci2Wwgslrln2FdYlaffzT_HMRJ4MsU0k')

# MADE BY NEPCODER @DEVSNP
required_channel = "@myserver23"

# MADE BY NEPCODER @DEVSNP
movie_api_url = 'https://moviedetails.apinepdev.workers.dev/'

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    is_member = check_membership(user_id)

    if is_member:
        bot.reply_to(message, "🎬 Welcome to the Movie Poster Bot! Send /movie <movie_name> to get movie details and posters. 📽️")
    else:
        join_button = InlineKeyboardButton("Join Channel 📢", url=f"https://t.me/myserver23")
        markup = InlineKeyboardMarkup().add(join_button)
        bot.send_message(message.chat.id, "🚫 To access the bot's features, please join our channel. Click the button below to join. 🚫", reply_markup=markup)

@bot.message_handler(commands=['movie'])
def get_movie_details(message):
    user_id = message.from_user.id
    is_member = check_membership(user_id)

    if is_member:
        try:
            movie_name = message.text.replace('/movie', '').strip()

  # MADE BY NEPCODER @DEVSNP
            response = requests.get(movie_api_url, params={'moviename': movie_name})

            if response.status_code == 200:
                movie_data = response.json()

      # MADE BY NEPCODER @DEVSNP
                poster_url = movie_data['Poster']
                if poster_url != 'N/A':
                    details_message = f"<b>📽️ Movie: {movie_name}</b>\n\n"
                    for key, value in movie_data.items():
                        if key != 'Poster':
                            details_message += f"<b>{key}:</b> {value}\n"
                    bot.send_photo(message.chat.id, poster_url, caption=details_message, parse_mode='HTML')
                else:
                    bot.reply_to(message, "❌ No poster available for this movie. ❌")
            else:
                bot.reply_to(message, "❌ Movie not found. Please check the movie name and try again. ❌")
        except Exception as e:
            bot.reply_to(message, "⚠️ An error occurred while fetching movie details. Please try again later. ⚠️")
    else:
        bot.reply_to(message, "🚫 You need to join our channel to access this command. Click the 'Join Channel' button to join. 🚫")

def check_membership(user_id):
    try:
        chat_member = bot.get_chat_member(chat_id=required_channel, user_id=user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except Exception as e:
        return False

bot.polling()

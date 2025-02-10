import logging
import random
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
TOKEN = "7610408338:AAHhSDWn0bz9IR5BGWlB8H_u7MUPH5963sg"
ADMIN_IDS = [7369976226]  # Add admin user IDs here
BANNED_USERS = set()
QUIZ_SCORES = {}

# Conversation states
QUIZ, MEME = range(2)

# Quiz questions
QUIZ_QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Paris", "Berlin", "Madrid"],
        "correct": 1
    },
    {
        "question": "Which planet is closest to the Sun?",
        "options": ["Venus", "Mars", "Mercury", "Earth"],
        "correct": 2
    }
]

# Start command
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\! I\'m a powerful bot with many features\!'
        '\n\nAvailable commands:'
        '\n/start - Start the bot'
        '\n/help - Show help'
        '\n/quiz - Start a quiz game'
        '\n/meme - Generate a random meme'
        '\n/dice - Roll a dice'
        '\n/ban - Ban a user (admin only)'
        '\n/uppercase <text> - Convert text to uppercase'
        '\n/joke - Get a random joke'
    )

# Help command
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Help Section:'
        '\n\nAdmin Commands:'
        '\n/ban - Ban a user (reply to message)'
        '\n/moderate - Delete messages with bad words'
        '\n\nUser Commands:'
        '\n/quiz - Play quiz game'
        '\n/dice - Roll a dice'
        '\n/joke - Get a random joke'
        '\n/meme - Generate meme'
        '\n/uppercase - Convert text to uppercase'
    )

# Ban command (admin only)
def ban_user(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id not in ADMIN_IDS:
        update.message.reply_text('⚠️ You are not authorized!')
        return

    reply = update.message.reply_to_message
    if reply:
        BANNED_USERS.add(reply.from_user.id)
        update.message.reply_text(f'🚫 User {reply.from_user.first_name} has been banned!')
    else:
        update.message.reply_text('Please reply to a message to ban the user.')

# Quiz game
def quiz(update: Update, context: CallbackContext) -> int:
    context.user_data['quiz_score'] = 0
    context.user_data['current_question'] = 0
    return ask_question(update, context)

def ask_question(update: Update, context: CallbackContext) -> int:
    question_index = context.user_data['current_question']
    question = QUIZ_QUESTIONS[question_index]
    
    keyboard = [
        [InlineKeyboardButton(option, callback_data=str(i))]
        for i, option in enumerate(question["options"])
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        f'Question {question_index + 1}: {question["question"]}',
        reply_markup=reply_markup
    )
    return QUIZ

def quiz_answer(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    
    question_index = context.user_data['current_question']
    correct_answer = QUIZ_QUESTIONS[question_index]["correct"]
    
    if int(query.data) == correct_answer:
        context.user_data['quiz_score'] += 1
        query.edit_message_text(text='✅ Correct!')
    else:
        query.edit_message_text(text='❌ Wrong!')
    
    context.user_data['current_question'] += 1
    
    if context.user_data['current_question'] < len(QUIZ_QUESTIONS):
        return ask_question(update, context)
    else:
        final_score = context.user_data['quiz_score']
        query.message.reply_text(
            f'Quiz finished! Your score: {final_score}/{len(QUIZ_QUESTIONS)}'
        )
        return ConversationHandler.END

# Meme generator
def meme(update: Update, context: CallbackContext) -> None:
    memes = [
        "https://i.imgflip.com/30b1gx.jpg",
        "https://i.imgflip.com/1g8my4.jpg",
        "https://i.imgflip.com/1ur9b0.jpg"
    ]
    update.message.reply_photo(random.choice(memes))

# Dice game
def dice(update: Update, context: CallbackContext) -> None:
    roll = random.randint(1, 6)
    update.message.reply_dice(emoji='🎲')
    update.message.reply_text(f'You rolled: {roll}')

# Uppercase converter
def uppercase(update: Update, context: CallbackContext) -> None:
    text = ' '.join(context.args).upper()
    update.message.reply_text(text)

# Joke command
def joke(update: Update, context: CallbackContext) -> None:
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
        "Why don't skeletons fight each other? They don't have the guts!"
    ]
    update.message.reply_text(random.choice(jokes))

# Error handler
def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update {update} caused error {context.error}')

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('ban', ban_user))
    dispatcher.add_handler(CommandHandler('dice', dice))
    dispatcher.add_handler(CommandHandler('uppercase', uppercase))
    dispatcher.add_handler(CommandHandler('joke', joke))
    dispatcher.add_handler(CommandHandler('meme', meme))

    # Quiz conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('quiz', quiz)],
        states={
            QUIZ: [CallbackQueryHandler(quiz_answer)]
        },
        fallbacks=[]
    )
    dispatcher.add_handler(conv_handler)

    # Error handler
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
# Default to port 5000 if PORT is not set in the environment
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

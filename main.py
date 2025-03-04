import telebot
from telebot import types
import re
import time

token = "7455544866:AAGiKHtoTnx5OurEwdF33bO-ozqXV6W3cdQ"

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    owner = types.InlineKeyboardButton("👨‍💻 Owner", url="tg://settings/mera_dost")
    channel = types.InlineKeyboardButton("📣 Channel", url="https://t.me/myserver23")
    chat = types.InlineKeyboardButton("👥 Chat", url="https://t.me/Pre_contact_bot")
    addme = types.InlineKeyboardButton("➕ Add Me To Your Group ➕", url="https://t.me/All_in_one_kaku_bot?startgroup=start")
    commands = types.InlineKeyboardButton("📝 Commands", callback_data="commands")
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(addme)
    markup.add(channel, chat)
    markup.add(owner, commands)
    
    bot.send_message(message.chat.id, """*🫶 Welcome To Help Bot!

🤖 My Names my server.

👨‍💻 My Developer* [my friend](tg://settings/mera_dost)

*🤖 Version* `1.0.1`""", parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "commands")
def commands_callback(call):
    commands = types.InlineKeyboardButton("🔙 Back", callback_data="back_menu")
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(commands)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""
*Bot Commands

👮🏻  /ban lets you ban a user from the group without giving him the possibility to join again using the link of the group

👮🏻  /unban lets you remove a user from group's blacklist, giving them the possibility to join again with the link of the group

👮🏻  /mute puts a user in read-only mode. He can read but he can't send any messages

👮🏻 /unmute removes a user from read-only mode

👮🏻  /kick bans a user from the group, giving him the possibility to join again with the link of the group

👮🏻  /info gives information about a user*
""", parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "back_menu")
def back_menu_callback(call):
  owner = types.InlineKeyboardButton("👨‍💻 Owner", url="tg://settings/mera_dost")
  channel = types.InlineKeyboardButton("📣 Channel", url="https://t.me/myserver23")
  chat = types.InlineKeyboardButton("👥 Chat", url="https://t.me/Pre_contact_bot")
  commands = types.InlineKeyboardButton("📝 Commands", callback_data="commands")
  markup = types.InlineKeyboardMarkup(row_width=2)
  markup.add(owner)
  markup.add(channel, chat)
  markup.add(commands)

  bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""*🫶 Welcome To Help Bot!

  🤖 My Names - my server.

  👨‍💻 My Developer* [my friend](tg://settings/mera_dost)

  *🤖 Version* `1.0.1`""", parse_mode="Markdown", reply_markup=markup)


@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_members(message):
    for user in message.new_chat_members:
        user_link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
        welcome_message = f"<b>🚀 Welcome {user_link} to the group! 🌟</b>"
        bot.send_message(message.chat.id, welcome_message, parse_mode="HTML")

@bot.message_handler(content_types=['left_chat_member'])
def left_member(message):
    user_link = f'<a href="https://t.me/{message.left_chat_member.username}">{message.left_chat_member.first_name}</a>'
    bot.send_message(message.chat.id, f"<b>😢 {user_link} has left the group.</b>", parse_mode="HTML", disable_web_page_preview=True)

####################################
# Group Security Command BY-Zexus #
###################################

@bot.message_handler(commands=['ban'])
def ban_user(message):
    chat_id = message.chat.id 
    user_id = message.from_user.id 
    admins = bot.get_chat_administrators(chat_id)  
    is_admin = False  
    can_ban = False  
    is_creator = False  

    for admin in admins:
        if admin.user.id == user_id:
            is_admin = True
            if admin.can_restrict_members:
                can_ban = True 
            if admin.status == "creator": 
                is_creator = True
            break 

    if (is_admin and can_ban) or is_creator:  
        if message.reply_to_message: 
            target_id = message.reply_to_message.from_user.id
        elif len(message.text.split()) > 1:
            target_id = int(message.text.split()[1]) 
        else: 
            bot.reply_to(message, "*❌ Please reply to the message of the user you want to ban or specify their user ID.*", parse_mode="Markdown") 
            return  
        if target_id == user_id:
            bot.reply_to(message, "*Ahahahaha Are You Serious?*", parse_mode="Markdown")
            return
        if target_id == 6724302593:
          bot.reply_to(message, "*Ahahahaha Are You Kidding Me?*", parse_mode="Markdown")
          return

        try: 
            bot.kick_chat_member(chat_id, target_id)
            bot.send_message(chat_id, f"*User Succesfully Banned! (*`{user_id}`*)*" , parse_mode="Markdown")
        except Exception as e:
            bot.reply_to(message, f"*Error:* `{e}`", parse_mode="Markdown")
    else:
        bot.reply_to(message, "*You Are Not Admin!*" , parse_mode="Markdown")
      

@bot.message_handler(commands=['unban'])
def unban_user(message):
    chat_id = message.chat.id 
    user_id = message.from_user.id 
    admins = bot.get_chat_administrators(chat_id)  
    is_admin = False  
    can_ban = False  
    is_creator = False  

    for admin in admins:
        if admin.user.id == user_id:
            is_admin = True
            if admin.can_restrict_members:
                can_ban = True 
            if admin.status == "creator": 
                is_creator = True
            break 

    if (is_admin and can_ban) or is_creator:  
        if message.reply_to_message: 
            target_id = message.reply_to_message.from_user.id
        elif len(message.text.split()) > 1:
            target_id = int(message.text.split()[1]) 
        else: 
          bot.reply_to(message, "*❌ Please reply to the message of the user you want to ban or specify their user ID.*", parse_mode="Markdown") 
          return  
          
        if target_id == user_id:
            bot.reply_to(message, "*Ahahahaha Are You Serious?*", parse_mode="Markdown")
            return
        if target_id == 6724302593:
          bot.reply_to(message, "*Ahahahaha Are You Kidding Me?*", parse_mode="Markdown")
          return

        target_status = bot.get_chat_member(chat_id, target_id).status
      
        if target_status in ["member", "administrator", "creator"]:
          bot.reply_to(message, "*User Already Unbanned!*", parse_mode="Markdown")
          return
        try: 
            bot.unban_chat_member(chat_id, target_id)  
            bot.send_message(chat_id, f"*User Succesfully Unbanned! (*`{user_id}`*)*" , parse_mode="Markdown") 
        except Exception as e:
            bot.reply_to(message, f"*Error*: `{e}`", parse_mode="Markdown") 
    else:
        bot.reply_to(message, "*You Are Not Admin!*" , parse_mode="Markdown") 


@bot.message_handler(commands=['mute'])
def mute_user(message):
    chat_id = message.chat.id 
    user_id = message.from_user.id 
    admins = bot.get_chat_administrators(chat_id)  
    is_admin = False  
    can_ban = False  
    is_creator = False  
    target_id = None
    duration = None

    for admin in admins:
        if admin.user.id == user_id:
            is_admin = True
            if admin.can_restrict_members:
                can_ban = True 
            if admin.status == "creator": 
                is_creator = True
            break 

    if (is_admin and can_ban) or is_creator:
        if message.reply_to_message: 
            target_id = message.reply_to_message.from_user.id
            time_match = re.search(r'(\d+)([mhd])', message.text)
            if time_match:
                amount, unit = time_match.groups()
                if unit == 'm':
                    duration = int(amount) * 60 
                elif unit == 'h':
                    duration = int(amount) * 3600
                elif unit == 'd':
                    duration = int(amount) * 86400 
        elif len(message.text.split()) > 1:
            target_id_match = re.search(r'(\d+)', message.text)
            if target_id_match:
                target_id = int(target_id_match.group(1))
                time_match = re.search(r'(\d+)([mhd])', message.text)
                if time_match:
                    amount, unit = time_match.groups()
                    if unit == 'm':
                        duration = int(amount) * 60 
                    elif unit == 'h':
                        duration = int(amount) * 3600
                    elif unit == 'd':
                        duration = int(amount) * 86400 
        else:
            bot.reply_to(message, "*❌ Please reply to the user's message you want to mute, specify their ID, or provide a mute duration.*", parse_mode="Markdown") 
            return  

        if len(str(target_id)) != 10:
          bot.reply_to(message, "*❌ Invalid ID. Please enter a valid ID.*", parse_mode="Markdown") 
          return

        if target_id == user_id or target_id == 6724302593:
            bot.reply_to(message, "*Ahahahaha Are You Kidding Me?*", parse_mode="Markdown")
            return

        try: 
            bot.restrict_chat_member(chat_id, target_id, can_send_messages=False, until_date=time.time() + (duration if duration else 0))
            if duration:
                bot.send_message(chat_id, f"*User Successfully Muted for {amount}{unit}! (User ID: *`{target_id}`*)*" , parse_mode="Markdown")
            else:
                bot.send_message(chat_id, f"*User Successfully Muted! (User ID: *`{target_id}`*)*" , parse_mode="Markdown")
        except Exception as e:
            bot.reply_to(message, f"*Error:* `{e}`", parse_mode="Markdown")
    else:
        bot.reply_to(message, "*You Are Not Admin!*" , parse_mode="Markdown")


@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    admins = bot.get_chat_administrators(chat_id)
    is_admin = False
    can_ban = False
    is_creator = False

    for admin in admins:
        if admin.user.id == user_id:
            is_admin = True
            if admin.can_restrict_members:
                can_ban = True
            if admin.status == "creator":
                is_creator = True
            break

    if (is_admin and can_ban) or is_creator:
        target_id = None

        if message.reply_to_message:
            target_id = message.reply_to_message.from_user.id
        elif len(message.text.split()) > 1:
            target_id = int(message.text.split()[1])

        if target_id is None:
            bot.reply_to(message, "*❌ Please reply to the message of the user you want to unmute or specify their user ID.*", parse_mode="Markdown")
            return

        if target_id == user_id:
            bot.reply_to(message, "*Ahahahaha Are You Serious?*", parse_mode="Markdown")
            return
        if target_id == 6724302593:
            bot.reply_to(message, "*Ahahahaha Are You Kidding Me?*", parse_mode="Markdown")
            return

        try:
            bot.restrict_chat_member(chat_id, target_id, can_send_messages=True)
            bot.send_message(chat_id, f"*User Successfully Unmuted! (*`{target_id}`*)*", parse_mode="Markdown")
        except Exception as e:
            bot.reply_to(message, f"*Error:* `{e}`", parse_mode="Markdown")
    else:
        bot.reply_to(message, "*You Are Not an Admin!*", parse_mode="Markdown")


@bot.message_handler(commands=['kick'])
def kick_user(message):
    chat_id = message.chat.id 
    user_id = message.from_user.id 
    admins = bot.get_chat_administrators(chat_id)  
    is_admin = False  
    can_ban = False  
    is_creator = False  

    for admin in admins:
        if admin.user.id == user_id:
            is_admin = True
            if admin.can_restrict_members:
                can_ban = True 
            if admin.status == "creator": 
                is_creator = True
            break 

    if (is_admin and can_ban) or is_creator:  
        if message.reply_to_message: 
            target_id = message.reply_to_message.from_user.id
        elif len(message.text.split()) > 1:
            target_id = int(message.text.split()[1]) 
        else: 
            bot.reply_to(message, "*❌ Please reply to the message of the user you want to kick or specify their user ID.*", parse_mode="Markdown") 
            return  
        if target_id == user_id:
            bot.reply_to(message, "*Ahahahaha Are You Serious?*", parse_mode="Markdown")
            return
        if target_id == 6724302593:
          bot.reply_to(message, "*Ahahahaha Are You Kidding Me?*", parse_mode="Markdown")
          return

        try: 
            bot.kick_chat_member(chat_id, target_id)
            bot.unban_chat_member(chat_id, target_id)
            bot.send_message(chat_id, f"*User Succesfully Kicked! (*`{user_id}`*)*" , parse_mode="Markdown")
        except Exception as e:
            bot.reply_to(message, f"*Error:* `{e}`", parse_mode="Markdown")
    else:
        bot.reply_to(message, "*You Are Not Admin!*" , parse_mode="Markdown")
      
@bot.message_handler(commands=['info'])
def info_user(message):
    user = None 

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.text.split()) > 1:
        try:
            user_id = int(message.text.split()[1])
            user = bot.get_chat_member(message.chat.id, user_id).user
        except (ValueError, IndexError):
            bot.reply_to(message, "*❌ Please reply to the message of the user you want to kick or specify their user ID.*", parse_mode="Markdown") 
            return
    else:
        bot.reply_to(message, f"*This Chat ID:* `{message.chat.id}`", parse_mode="Markdown")
    user_link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
    user_info_text = f"<b>User ID:</b> <code>{user.id}</code>\n<b>Username: @{user.username}\nFirst Name: {user.first_name}\nLast Name: {user.last_name}\nUser Link: {user_link}</b>"
    bot.reply_to(message, user_info_text, parse_mode="HTML")

####################################
# Group Security Command BY-Zexus #
###################################

bot.infinity_polling()

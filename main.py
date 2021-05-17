import telebot

API_TOKEN = "1829309173:AAEwaLKc-7UX57EsjdyWfYx-PDlEAO9lEo0"
LANGUAGES = ["English", "Russian", "Turkish", "Italian", "French"]
language_from = ""
language_to = ""

bot = telebot.TeleBot(API_TOKEN)

def create_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    for language in LANGUAGES:
        markup.add(telebot.types.InlineKeyboardButton(text=language, callback_data=language))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Thanks for starting me, {message.from_user.first_name}.'
                     ' I am ready to help you whenever you need. Type /set_languages to continue')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Available Commands:\n/start\n/help\n/set_languages')


@bot.message_handler(commands=['set_languages'])
def set_languages(message):
    bot.send_message(message.chat.id, "Choose the language to translate from:", reply_markup=create_markup())


@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    pass

# def get_language_from(message):
#     global language_from
#     language_from = message.text
#     bot.send_message(message.chat.id, "Choose the language to translate to:", reply_markup=create_markup())
#     bot.register_next_step_handler_by_chat_id(message.chat.id, get_language_to)
#
#
# def get_language_to(message):
#     global language_to
#     language_to = message.text
#     bot.send_message(message.chat.id, f"You have chosen: {language_from} to {language_to}")

bot.polling()

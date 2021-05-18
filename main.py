import telebot
from telebot import types
import requests

class Translator:
    def __init__(self):
        self.url = "https://microsoft-translator-text.p.rapidapi.com/translate"
        self.headers = {
            'content-type': "application/json",
            'x-rapidapi-key': "c28aab65bemsh3af2835d9a7e605p1888d2jsn3fa6e41a92ec",
            'x-rapidapi-host': "microsoft-translator-text.p.rapidapi.com"
        }
        self.original_language = ""
        self.target_language = ""

    def translate(self, text):
        body = [{'text': text}]
        params = {
            'api-version': '3.0',
            'from': self.original_language,
            'to': self.target_language
        }

        request = requests.post(self.url, params=params, headers=self.headers, json=body)
        response = request.json()
        return response[0]["translations"][0]["text"]


API_TOKEN = "1829309173:AAEwaLKc-7UX57EsjdyWfYx-PDlEAO9lEo0"
LANGUAGES = {"English": 'en', "Russian": 'ru', "Turkish": 'tr', "Italian": 'it', "French": 'fr', "Albanian":'AL'}
bot = telebot.TeleBot(API_TOKEN)
translator = Translator()


def create_markup(function_name):
    markup = types.InlineKeyboardMarkup()
    for language in LANGUAGES:
        lang_code = LANGUAGES[language]
        markup.add(types.InlineKeyboardButton(text=language, callback_data=f'{function_name}-{lang_code}'))
    return markup


def get_from_callback(query):
    bot.answer_callback_query(query.id)
    translator.original_language = query.data.split('-')[1]


def get_to_callback(query):
    bot.answer_callback_query(query.id)
    translator.target_language = query.data.split('-')[1]


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Thanks for starting me, {message.from_user.first_name}. '
                                      'I am ready to help you whenever you need. Press /help to see available commands')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Available Commands:\n/start\n/help\n/set_language_from'
                                      '\n/set_language_to\n/get_current_languages\n/translate')


@bot.message_handler(commands=['set_language_from'])
def set_language_from(message):
    bot.send_message(message.chat.id, "Choose the language to translate from:", reply_markup=create_markup('from'))


@bot.message_handler(commands=['set_language_to'])
def set_language_to(message):
    bot.send_message(message.chat.id, "Choose the language to translate to:", reply_markup=create_markup('to'))


@bot.message_handler(commands=['get_current_languages'])
def get_current_languages(message):
    bot.send_message(message.chat.id, f"{translator.original_language} ---> {translator.target_language}")


@bot.message_handler(commands=['translate'])
def translate(message):
    if translator.target_language == "":
        bot.send_message(message.chat.id, "Set a language to translate to /set_language_to")
    else:
        response = message.reply_to_message
        text_to_translate = response.json['text']
        translation = translator.translate(text_to_translate)
        bot.reply_to(message, translation)

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    if 'from' in data:
        get_from_callback(query)
    elif 'to' in data:
        get_to_callback(query)
    else:
        print(f"error happened : {data}")

bot.polling()

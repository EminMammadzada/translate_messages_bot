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

    def translate(self, text, from_lang, to_lang):
        body = [{'text': text}]
        params = {
            'api-version': '3.0',
            'from': from_lang,
            'to': to_lang
        }

        request = requests.post(self.url, params=params, headers=self.headers, json=body)
        response = request.json()
        return response[0]["translations"][0]["text"]


API_TOKEN = "1829309173:AAEwaLKc-7UX57EsjdyWfYx-PDlEAO9lEo0"
LANGUAGES = ["English", "Russian", "Turkish", "Italian", "French"]
language_from = ""
language_to = ""
bot = telebot.TeleBot(API_TOKEN)
translator = Translator()


def create_markup(function_name):
    markup = types.InlineKeyboardMarkup()
    for language in LANGUAGES:
        markup.add(types.InlineKeyboardButton(text=language, callback_data=f'{function_name}-{language}'))
    return markup


def get_from_callback(query):
    global language_from
    bot.answer_callback_query(query.id)
    language_from = query.data.split('-')[1]


def get_to_callback(query):
    global language_to
    bot.answer_callback_query(query.id)
    language_to = query.data.split('-')[1]


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
    global language_from
    global language_to
    bot.send_message(message.chat.id, f"{language_from} ---> {language_to}")


@bot.message_handler(commands=['translate'])
def translate(message):
    if language_to == "":
        bot.send_message(message.chat.id, "Set a language to translate to /set_language_to")

    else:
        pass

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    global language_from
    global language_to
    data = query.data
    if 'from' in data:
        get_from_callback(query)
    elif 'to' in data:
        get_to_callback(query)
    else:
        print(f"error happened : {data}")


bot.polling()

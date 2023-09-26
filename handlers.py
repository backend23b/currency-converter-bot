from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from db import UserDB
import requests

users_db = UserDB('db.json')


currency_keyboard = [
    [InlineKeyboardButton('UZS', callback_data='UZS'), InlineKeyboardButton('EUR', callback_data='EUR')],
    [InlineKeyboardButton('USD', callback_data='USD'), InlineKeyboardButton('RUB', callback_data='RUB')],
]


def start(update: Update, context: CallbackContext):
    user = update.effective_user

    users_db.add_user(chat_id=user.id, first_name=user.first_name, last_name=user.last_name, username=user.username)

    update.message.reply_html(
        text=f'Hello, {user.full_name}! Welcome to Currency Converter Bot.'
    )

    update.message.reply_html(
        text=f'Select your Currency.',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=currency_keyboard)
    )

def currency(update: Update, context: CallbackContext):
    data = update.callback_query.data

    users_db.add_currency(chat_id=update.effective_user.id, currency=data)

    update.callback_query.message.reply_html(
        text='Send amount of your money.'
    )

def convert(update: Update, context: CallbackContext):
    data = update.message.text

    amount = float(data)
    base = users_db.users.get(doc_id=update.effective_user.id)['currency']

    url = "http://127.0.0.1:5000/api/v1/convert/"

    payload = {'amount': amount, 'base': base}


    response = requests.get(url, params=payload)

    resp = ''
    for x in response.json():
        resp += f"<b>{x['currency']}</b>: {x['value']}\n"

    update.message.reply_html(
        text=resp
    )

import telebot
import webbrowser
from telebot import types
import sqlite3
import requests
import json
from currency_converter import CurrencyConverter

TOKEN = '7182161349:AAFG6p9F2bxfM4tFAnVeuERKpg5HfcsaYXg'
API = '19467d303309e34f0e6e2908b862a06e'

bot = telebot.TeleBot(TOKEN)
name = None

currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    mark_up = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Додаємо resize_keyboard=True для зручності
    btn1 = types.KeyboardButton('Weather info')
    btn2 = types.KeyboardButton('Change currency')
    btn3 = types.KeyboardButton('Want to register?')
    mark_up.add(btn1, btn2, btn3)  # Можна додати всі кнопки в один рядок або різні рядки
    
    bot.send_message(message.chat.id, 'Hello, it’s a help bot market! 😄', reply_markup=mark_up)
    bot.send_message(message.chat.id, 'And we can tell the weather, convert currency.')

@bot.message_handler(func=lambda message: message.text in ['Weather info', 'Change currency', 'Want to register?'])
def on_click(message):
    if message.text == 'Weather info':
        bot.send_message(message.chat.id, 'Type /weather and the city name to get weather info.')
    elif message.text == 'Change currency':
        bot.send_message(message.chat.id, 'Type /convert to start the currency conversion.')
    elif message.text == 'Want to register?':
        bot.send_message(message.chat.id, 'Type /reg to start the registration process.')

def on_clik(message):
    if message.text == 'want to register?':
        bot.send_message(message.chat.id, 'type /reg')
    elif message.text == 'cange curency':
        bot.send_message(message.chat.id, 'type /convert')

    elif message.text == 'Weather info':
        bot.send_message(message.chat.id, 'Type /weather and any cyti, and get your weather info')

@bot.message_handler(commands=['reg'])
def register(message):
    bot.send_message(message.chat.id, 'Registration')
    bot.send_message(message.chat.id, 'Type your name')
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Type your password')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    passnonh = message.text.strip()
    password = hash(passnonh)
    conn = sqlite3.connect('baza.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users(name, pass) VALUES(?, ?)", (name, password))

    conn.commit()
    cur.close()
    conn.close()

    mark_up = types.InlineKeyboardMarkup()
    btn1 = (types.InlineKeyboardButton('Users List:', callback_data='users'))
    mark_up.row(btn1)
    bot.send_message(message.chat.id, 'You have been registered', reply_markup=mark_up)

# ALL USERS DATA
# @bot.callback_query_handler(func=lambda call: True)
# def callback(call):
#     conn = sqlite3.connect('baza.sql')
#     cur = conn.cursor()

#     cur.execute('SELECT * FROM users')
    
#     users = cur.fetchall()

#     info = ''
#     for el in users:
#         info += f'Name: {el[1]}, password: {el[2]}\n'

#     cur.close()
#     conn.close()

#     bot.send_message(call.message.chat.id, info)

@bot.message_handler(commands=['convert'])
def convert(message):
    bot.send_message(message.chat.id, 'Enter sum')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = float(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'INVALID DATA, please provide correct data.')
        bot.register_next_step_handler(message, summa)
        return
    
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
    btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
    btn3 = types.InlineKeyboardButton('EUR/UAH', callback_data='eur/uah')
    btn4 = types.InlineKeyboardButton('UAH/EUR', callback_data='uah/eur')
    btn_cust = types.InlineKeyboardButton('Custom convert', callback_data='else')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4) 
    markup.row(btn_cust)
    bot.send_message(message.chat.id, 'Choose a currency pair', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        try:
            res = currency.convert(amount, values[0], values[1])
            bot.send_message(call.message.chat.id, f'Result: {round(res, 2)}. You can try convert again.')
        except Exception as e:
            bot.send_message(call.message.chat.id, f'Error: {str(e)}')
    else:
        bot.send_message(call.message.chat.id, 'Type your currency pair like this: USD/EUR')
        bot.register_next_step_handler(call.message, summa)

def my_currency(message):
    try:
        values = message.text.upper().split('/')
        if len(values) != 2:
            raise ValueError('Invalid format. Please use the format: USD/EUR')
        
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Result: {round(res, 2)}. You can try convert again.')
    except Exception as e:
        bot.send_message(message.chat.id, f'Error: {str(e)}. Please provide correct data.')
        bot.register_next_step_handler(message, my_currency)

@bot.message_handler(commands=[ 'help'])
def send_help(message):
     bot.send_message(message.chat.id, "<b>Help information here(contact +<u>380-63-440-4800</u>)</b>", parse_mode = "html")

@bot.message_handler(commands=[ 'bay'])
def pass_bay(message):
    mark_up = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('bay aksepted', url='https://www.google.com/search')
    mark_up.row(btn1)
    btn2 = types.InlineKeyboardButton('bay decline', callback_data='delete')
    btn3 = types.InlineKeyboardButton('editt ofer', callback_data='edit')
    mark_up.row(btn2, btn3)
    # mark_up.add(types.InlineKeyboardButton('bay aksepted', url='https://www.google.com/search'))
    # mark_up.add(types.InlineKeyboardButton('bay decline', callback_data='send'))
    # mark_up.add(types.InlineKeyboardButton('editt ofer', callback_data='edit'))
    bot.reply_to(message, "want to bay a produkt?", reply_markup=mark_up)

@bot.callback_query_handler(func = lambda callback: True)
def callback_message(callback):
    if callback.data == "delete" :
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
    elif callback == "edit":
        bot.edit_message_text('Edit message', callback.message.chat.id, callback.message.message_id - 1)



@bot.message_handler(commands=['weather'])
def woather_star(message):
    bot.send_message(message.chat.id, 'Type Cyti')
    bot.register_next_step_handler(message, weatger_info)

def weatger_info(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'Temperatur now is: {data["main"]["temp"]}')

        image = 'sune.png' if temp > 5.0 else 'cloudy.png'
        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, 'Cyti is ERROR, pleas try corecktli cyti name.')

bot.infinity_polling()
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import uuid
import threading
import os
from flask import Flask

# Replace with your actual bot token
API_TOKEN = '8792860370:AAHCNwe0F9Lf-B9NoPyCZYpUDF8R5YAjoeA'

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# This dummy web server allows free hosting platforms (like Render) to host your bot without errors.
@app.route('/')
def home():
    return "Bot is running!"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Generate a unique ID for the user
    unique_id = str(uuid.uuid4()).split('-')[0].upper()
    
    welcome_text = (
        f"🏦 Welcome to the Banking Leads Hub!\n\n"
        f"Your unique Customer ID is: *{unique_id}*\n\n"
        f"Please choose a plan to view our exclusive banking leads:"
    )
    
    # Create inline keyboard for plan options
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Platinum - 349$", callback_data="plan_platinum"),
        InlineKeyboardButton("Silver - 499$", callback_data="plan_silver"),
        InlineKeyboardButton("Gold - 649$", callback_data="plan_gold")
    )
    
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # Handle callback queries from inline keyboard
    if call.data == "plan_platinum":
        bot.answer_callback_query(call.id, "You selected Platinum")
        bot.send_message(call.message.chat.id, "💎 *Platinum Plan* selected.\nPrice: 349$\n\nContact the admin to proceed with the payment and receive your leads.", parse_mode="Markdown")
    elif call.data == "plan_silver":
        bot.answer_callback_query(call.id, "You selected Silver")
        bot.send_message(call.message.chat.id, "🥈 *Silver Plan* selected.\nPrice: 499$\n\nContact the admin to proceed with the payment and receive your leads.", parse_mode="Markdown")
    elif call.data == "plan_gold":
        bot.answer_callback_query(call.id, "You selected Gold")
        bot.send_message(call.message.chat.id, "🥇 *Gold Plan* selected.\nPrice: 649$\n\nContact the admin to proceed with the payment and receive your leads.", parse_mode="Markdown")

if __name__ == '__main__':
    # Start the Flask web server in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    
    print("Bot is running...")
    # Keep the bot running infinitely
    bot.infinity_polling()

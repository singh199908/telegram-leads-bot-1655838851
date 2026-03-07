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

# Dictionary to store users who have redeemed the platinum plan
premium_users = {}
all_users = {}

REDEEM_CODE = "8cfxUgwa97t0OaAb3343gaX"

# Dummy web server for free hosting platforms (like Render)
@app.route('/')
def home():
    return "Bot is running!"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    unique_id = str(uuid.uuid4()).split('-')[0].upper()
    user_id = message.from_user.id
    
    # Register user
    if user_id not in all_users:
        all_users[user_id] = {
            "first_name": message.from_user.first_name,
            "username": message.from_user.username,
            "unique_id": unique_id
        }
        
    # If user already redeemed the code, skip to the premium menu
    if premium_users.get(user_id):
        show_bank_menu(message.chat.id)
        return
        
    welcome_text = (
        f"🏦 Welcome to the Banking Leads Hub!\n\n"
        f"Your unique Customer ID is: *{unique_id}*\n\n"
        f"Please choose a plan to view our exclusive banking leads:\n"
        f"_(Or use /redeem <code> if you have an access code)_"
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

@bot.message_handler(commands=['redeem'])
def redeem_code(message):
    user_id = message.from_user.id
    
    # Check if they sent /redeem <code>
    args = message.text.split()
    if len(args) < 2:
        bot.send_message(message.chat.id, "⚠️ *Error:* Please provide a code.\n\nExample: `/redeem 8cfxUgwa97t0OaAb3343gaX`", parse_mode="Markdown")
        return
        
    code = args[1]
    
    # Verify the code
    if code == REDEEM_CODE:
        premium_users[user_id] = True
        bot.send_message(message.chat.id, "✅ *Platinum plan is enabled!*\n\nYou now have access to our premium USA banking leads database.", parse_mode="Markdown")
        show_bank_menu(message.chat.id)
    else:
        bot.send_message(message.chat.id, "❌ *Invalid code!* Please check your access code and try again.", parse_mode="Markdown")

@bot.message_handler(commands=['users'])
def list_users(message):
    # This shows the list of all users who used the bot
    if not all_users:
        bot.send_message(message.chat.id, "No users have started the bot yet.")
        return
        
    user_list = "👥 *Registered Users:*\n\n"
    for uid, data in all_users.items():
        username = f"@{data['username']}" if data.get('username') else "No Username"
        status = "💎 Premium" if premium_users.get(uid) else "🆓 Free"
        user_list += f"• ID: {data['unique_id']} | Name: {data.get('first_name')} | {username} | {status}\n"
        
    bot.send_message(message.chat.id, user_list, parse_mode="Markdown")

def show_bank_menu(chat_id):
    menu_text = "🏦 *Premium USA Banks Database*\n\nPlease select a bank to view available leads:"
    
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("🏦 Chase", callback_data="bank_chase"),
        InlineKeyboardButton("🏦 Bank of America", callback_data="bank_boa"),
        InlineKeyboardButton("🏦 Wells Fargo", callback_data="bank_wells"),
        InlineKeyboardButton("🏦 Citibank", callback_data="bank_citi"),
        InlineKeyboardButton("🏦 US Bank", callback_data="bank_usbank"),
        InlineKeyboardButton("🏦 PNC Bank", callback_data="bank_pnc"),
        InlineKeyboardButton("🏦 Truist", callback_data="bank_truist"),
        InlineKeyboardButton("🏦 Capital One", callback_data="bank_capitalone"),
        InlineKeyboardButton("🏦 TD Bank", callback_data="bank_td")
    )
    # Add a close/logout button if you want
    markup.add(InlineKeyboardButton("❌ Exit Menu", callback_data="exit_menu"))
    
    bot.send_message(chat_id, menu_text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # Handle plan selections
    if call.data.startswith("plan_"):
        plan_names = {
            "plan_platinum": "💎 *Platinum Plan*\nPrice: 349$",
            "plan_silver": "🥈 *Silver Plan*\nPrice: 499$",
            "plan_gold": "🥇 *Gold Plan*\nPrice: 649$"
        }
        plan_text = plan_names.get(call.data, "Plan selected")
        bot.answer_callback_query(call.id, "Processing...")
        bot.send_message(call.message.chat.id, f"{plan_text}\n\nContact the admin to proceed with the payment and receive your leads.", parse_mode="Markdown")
    
    # Handle bank selections for premium users
    elif call.data.startswith("bank_"):
        bank_names = {
            "bank_chase": "Chase", "bank_boa": "Bank of America", "bank_wells": "Wells Fargo",
            "bank_citi": "Citibank", "bank_usbank": "US Bank", "bank_pnc": "PNC Bank",
            "bank_truist": "Truist", "bank_capitalone": "Capital One", "bank_td": "TD Bank"
        }
        
        bank = bank_names.get(call.data, "Selected Bank")
        bot.answer_callback_query(call.id, f"Fetching {bank} leads...")
        
        mock_leads = (
            f"📊 *{bank} Leads Available:*\n\n"
            f"✅ *Status:* High Quality | CC/Logins\n"
            f"🏢 *Checking Accounts:* {uuid.uuid4().int % 2000 + 500:,}\n"
            f"💳 *Credit Cards:* {uuid.uuid4().int % 1500 + 300:,}\n"
            f"📈 *Business Accounts:* {uuid.uuid4().int % 800 + 100:,}\n\n"
            f"🔗 Contact Admin `[@leadshub_admin]` to request data export."
        )
        bot.send_message(call.message.chat.id, mock_leads, parse_mode="Markdown")
        
    elif call.data == "exit_menu":
        bot.answer_callback_query(call.id, "Menu closed")
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

if __name__ == '__main__':
    # Start the web server purely to satisfy Render
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    print("Bot is running...")
    # Keep the bot running infinitely
    bot.infinity_polling()

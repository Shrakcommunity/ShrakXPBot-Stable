import telebot
import json
import os
import time

# 👇 Ajoute cette ligne pour garder le bot actif sur Render
from keep_alive import keep_alive
keep_alive()

# 🔐 Your BotFather token here
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
DATA_FILE = 'xp_data.json'

# 📥 Load data (with error handling)
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ JSON file corrupted or empty. Starting fresh.")
            return {}
    return {}

# 💾 Save data
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# 🧠 Titles based on level
def get_title(level):
    if level < 5:
        return "Baby Shraker 🐣"
    elif level < 10:
        return "Tide Explorer 🪸"
    elif level < 15:
        return "Bubble Talker 🗨️"
    elif level < 20:
        return "Abyss Diver 🧭"
    elif level < 30:
        return "Ocean Rider 🌊"
    else:
        return "Dragon of the Abyss 🐉"

# 📊 /level command (auto-delete, safe)
@bot.message_handler(commands=['level'])
def level_command(message):
    user_id = str(message.from_user.id)
    data = load_data()

    if user_id not in data:
        sent = bot.send_message(message.chat.id, "You haven't earned any XP yet. Start sending messages!")
        time.sleep(3)
        bot.delete_message(chat_id=message.chat.id, message_id=sent.message_id)
        return

    xp = data[user_id]["xp"]
    level = data[user_id]["level"]
    title = get_title(level)

    sent = bot.send_message(message.chat.id, f"📈 Your current level:\n\n🏅 Level: {level}\n🧪 XP: {xp}\n🎖 Title: {title}")
    time.sleep(3)
    bot.delete_message(chat_id=message.chat.id, message_id=sent.message_id)

# 🏆 /top command (auto-delete)
@bot.message_handler(commands=['top'])
def top_command(message):
    data = load_data()
    sorted_users = sorted(data.items(), key=lambda x: x[1].get("xp", 0), reverse=True)[:10]

    msg = "🏆 Top 10 most active members:\n"
    for i, (user_id, info) in enumerate(sorted_users, start=1):
        level = info["xp"] // 10
        title = get_title(level)

        if info.get("username"):
            mention = f"@{info['username']}"
        elif info.get("firstname"):
            mention = info['firstname']
        else:
            mention = "Anonymous"

        msg += f"{i}. {mention} – Lv {level} – {title}\n"

    sent = bot.send_message(message.chat.id, msg)
    time.sleep(3)
    bot.delete_message(chat_id=message.chat.id, message_id=sent.message_id)

# 🧪 Handle XP and level up messages with logging
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.chat.type not in ['group', 'supergroup']:
        return

    user_id = str(message.from_user.id)
    username = message.from_user.username
    firstname = message.from_user.first_name
    data = load_data()

    if user_id not in data:
        data[user_id] = {"xp": 0, "level": 0, "username": username, "firstname": firstname}
    else:
        data[user_id]["username"] = username
        data[user_id]["firstname"] = firstname

    print(f"[LOG] User {user_id} – @{username} / {firstname}")

    data[user_id]["xp"] += 1
    new_level = data[user_id]["xp"] // 10

    if new_level > data[user_id]["level"]:
        data[user_id]["level"] = new_level
        title = get_title(new_level)

        if username:
            mention = f"@{username}"
        else:
            mention = firstname or "Someone"

        bot.send_message(
            message.chat.id,
            f"🎉 {mention} just reached level {new_level} – {title}\nKeep it up!"
        )

    save_data(data)

# ▶️ Start the bot
print("🔥 ShrakXP Bot is running...")
try:
    print("✅ Bot is polling now...")
    bot.polling(none_stop=True)
except Exception as e:
    print(f"❌ Bot crashed with error: {e}")


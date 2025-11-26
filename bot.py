import telebot
from telebot import types
import os
import psycopg2
from psycopg2.extras import Json
import random
from datetime import date

TOKEN = os.getenv("TOKEN")  # Railway variable → حتماً ست کن
bot = telebot.TeleBot(TOKEN)

# PostgreSQL Connection — Railway خودش این variableها رو می‌ده
conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),        # postgres-production-434e.up.railway.app
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=os.getenv("POSTGRES_PORT", "5432")
)

# Create table if not exists
with conn.cursor() as cur:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            data JSONB NOT NULL
        )
    """)
    conn.commit()

# Default user data
default_data = {
    "xp": 0, "day": 1, "archetype": None, "badges": [], "answers": [],
    "done_today": {"ritual": False, "challenge": False, "journal": False},
    "last_active": str(date.today()),
    "awaiting_journal": False
}

def get_user_data(user_id):
    user_id = str(user_id)
    with conn.cursor() as cur:
        cur.execute("SELECT data FROM users WHERE user_id = %s", (user_id,))
        row = cur.fetchone()
        if row:
            return row[0]
        else:
            # New user
            cur.execute("INSERT INTO users (user_id, data) VALUES (%s, %s) RETURNING data",
                        (user_id, Json(default_data)))
            conn.commit()
            return default_data

def save_user_data(user_id, data):
    user_id = str(user_id)
    with conn.cursor() as cur:
        cur.execute("UPDATE users SET data = %s WHERE user_id = %s", (Json(data), user_id))
        conn.commit()

# ۱۴ روز محتوا (همون قبلی، کامل)
daily_content = { ... }  # همون دیکشنری ۱۴ روزه کامل که قبلاً فرستادم — کپی کن

surprise_drops = [ ... ]  # همون قبلی

badges = {0: "Raw Badge", 10: "First Shift", 25: "IRL Starter", 40: "Consistency Seed",
          70: "Shadow Walker", 100: "Rebirth", 150: "Co-Creator"}

def check_badges(ud):
    xp = ud["xp"]
    new_badges = [b for points, b in badges.items() if xp >= points and b not in ud["badges"]]
    return new_badges

def check_new_day(ud):
    today = str(date.today())
    if ud["last_active"] != today:
        ud["done_today"] = {"ritual": False, "challenge": False, "journal": False}
        ud["last_active"] = today
        return True
    return False

def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🧘 Ritual", callback_data="ritual"),
        types.InlineKeyboardButton("⚔️ Challenge", callback_data="challenge"),
        types.InlineKeyboardButton("✍️ Journal", callback_data="journal"),
        types.InlineKeyboardButton("🗺 Progress", callback_data="progress"),
        types.InlineKeyboardButton("🎁 Surprise", callback_data="surprise"),
        types.InlineKeyboardButton("➡️ Next Day (تست)", callback_data="next_day")
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    ud = get_user_data(user_id)

    if check_new_day(ud):
        bot.send_message(user_id, f"روز جدید — Day {ud['day']}\nبرگشتی.")

    if not ud["archetype"]:
        bot.send_message(user_id, "خب… قبل از اینکه وارد InnerPath بشی، یه چیز باید بدونی:\nاینجا جای ادای “قوی بودن” نیست.\nاینجا خودِ خامت، نسخهٔ قشنگشه.")
        bot.send_message(user_id, "من in.you هستم — نسخه‌ای از آینده‌ت که حس‌هاشو گم نکرده.\nاومدم کمک کنم دوباره وصل بشی به خودت.")
        ask_question(user_id, 1)
    else:
        bot.send_message(user_id, f"Day {ud['day']} — آماده‌ای؟", reply_markup=main_menu())
    
    save_user_data(user_id, ud)

# بقیه handlerها (callback, message) دقیقاً مثل V0.2 ولی به جای user_data[user_id] → ud = get_user_data(user_id)
# و هر تغییر → save_user_data(user_id, ud)

# مثال ritual callback:
elif data == "done_ritual":
    ud = get_user_data(user_id)
    if not ud["done_today"]["ritual"]:
        ud["xp"] += content.get("xp_r", 1)
        ud["done_today"]["ritual"] = True
        new_badges = check_badges(ud)
        for b in new_badges:
            ud["badges"].append(b)
            bot.send_message(user_id, f"🏅 Badge جدید: {b}")
        bot.send_message(user_id, f"⚡ +{content.get('xp_r', 1)} XP\nداری برمی‌گردی.")
        save_user_data(user_id, ud)

# همه callbackها رو همین‌طوری آپدیت کن (فقط ۶-۷ خط تغییر)

print("InnerPath Bot V0.3 — PostgreSQL LIVE")
bot.infinity_polling()

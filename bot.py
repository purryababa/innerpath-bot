import telebot
from telebot import types
import os
import psycopg2
from psycopg2.extras import Json
import random
from datetime import date

# ============= SECURITY FIX: NO HARDCODED TOKEN =============
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("No bot token found. Set TELEGRAM_BOT_TOKEN environment variable.")
bot = telebot.TeleBot(TOKEN)

# PostgreSQL Connection (Railway auto-provides these)
conn = psycopg2.connect(
    host=os.getenv("PGHOST"),           # یا POSTGRES_HOST اگر متفاوت بود
    database=os.getenv("PGDATABASE"),
    user=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    port=os.getenv("PGPORT", "5432")
)

# Create table
with conn.cursor() as cur:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            data JSONB NOT NULL
        )
    """)
    conn.commit()

default_data = {
    "xp": 0, "day": 1, "archetype": None, "badges": [], "answers": [],
    "done_today": {"ritual": False, "challenge": False, "journal": False},
    "last_active": str(date.today()), "awaiting_journal": False
}

# کامل ۱۴ روز محتوا — خام و تاریک
daily_content = {
    1: {"ritual": "۹۰ ثانیه نفس عمیق — ۴ داخل، ۲ نگه‌دار، ۶ بیرون", "challenge": "به شانه‌هات توجه کن — کجا تنش داری؟", "journal": "کجای بدنم بیشترین تنش رو داره؟", "xp_r": 1, "xp_c": 3, "xp_j": 2, "fragment": "in.you: تنش یعنی هنوز زنده‌ای."},
    2: {"ritual": "۴-۲-۶ شمارش نفس", "challenge": "۳ تا فکر اصلی امروزت رو بنویس", "journal": "این فکرا از کجا میان؟", "xp_r": 1, "xp_c": 3, "xp_j": 2, "fragment": "in.you: فکرها مهمونن. تو خونه نیستی."},
    3: {"ritual": "۱۵ ثانیه شونه‌ها رو تکون بده", "challenge": "۳ دقیقه پیاده‌روی بدون موبایل", "journal": "تو پیاده‌روی چی حس کردی؟", "xp_r": 1, "xp_c": 4, "xp_j": 2, "fragment": "in.you: بدن داره فریاد می‌زنه. گوش کن."},
    4: {"ritual": "دست روی قلب — ۳ بار بگو: من اینجام", "challenge": "یه جمله حقیقت خام با صدا بگو", "journal": "اون جمله چی بود؟", "xp_r": 1, "xp_c": 3, "xp_j": 3, "fragment": "in.you: حقیقت همیشه می‌سوزونه."},
    5: {"ritual": "تنفس لرزشی — بدن رو بلرزون", "challenge": "۳ دقیقه فقط نگاه به اطراف", "journal": "چی دیدی که قبلاً ندیده بودی؟", "xp_r": 1, "xp_c": 5, "xp_j": 2, "fragment": "in.you: دنیا منتظر توئه."},
    6: {"ritual": "نفس عمیق + آهــــ با صدا", "challenge": "یه جمله بنویس و پاره‌ش کن", "journal": "چی رو رها کردی؟", "xp_r": 1, "xp_c": 3, "xp_j": 3, "fragment": "in.you: رها کردن یعنی آزادی."},
    7: {"ritual": "چک‌این کامل بدن-فکر-احساس", "challenge": "همه هفته رو مرور کن", "journal": "چی تغییر کرد؟", "xp_r": 3, "xp_c": 4, "xp_j": 4, "fragment": "in.you: این فقط شروعه."},
    8: {"ritual": "Shadow Breath — ۲ دقیقه چشم‌بسته", "challenge": "بدترین ترست رو بنویس", "journal": "ترس چی می‌خواد بهت بگه؟", "xp_r": 3, "xp_c": 6, "xp_j": 4, "fragment": "in.you: سایه‌ات راهنماته."},
    9: {"ritual": "Anger Release — ۲۰ ثانیه مشت به بالش", "challenge": "پیام صوتی خشمگین (پاک کن)", "journal": "خشم زیرش چی بود؟", "xp_r": 3, "xp_c": 7, "xp_j": 4, "fragment": "in.you: خشم یعنی هنوز جنگجویی."},
    10: {"ritual": "خودتو ۹۰ ثانیه بغل کن", "challenge": "به یه غریبه لبخند بزن", "journal": "تنهایی الان چه شکلیه؟", "xp_r": 3, "xp_c": 6, "xp_j": 5, "fragment": "in.you: تنهایی یعنی جای خودت خالیه."},
    11: {"ritual": "همه فکرا رو بنویس و بسوزون", "challenge": "۱۰ دقیقه سکوت مطلق", "journal": "بدون فکر چی موند؟", "xp_r": 3, "xp_c": 5, "xp_j": 5, "fragment": "in.you: سکوت = خود واقعی."},
    12: {"ritual": "Body Scan از انگشت پا تا سر", "challenge": "رقص احمقانه جلوی آینه", "journal": "بدنت چی می‌گه؟", "xp_r": 3, "xp_c": 6, "xp_j": 4, "fragment": "in.you: بدن دروغ نمی‌گه."},
    13: {"ritual": "Forgiveness Breath — به خودت ببخش", "challenge": "نامه به خود ۱۰ سال پیش", "journal": "چی می‌خواستی بشنوی؟", "xp_r": 4, "xp_c": 7, "xp_j": 6, "fragment": "in.you: بخشش = آزادی."},
    14: {"ritual": "Rebirth — همه ۱۴ روز رو مرور کن", "challenge": "Ritual شخصی بساز", "journal": "من دیگه کی‌ام؟", "xp_r": 10, "xp_c": 10, "xp_j": 10, "fragment": "in.you: تو متولد شدی. دوباره."}
}

surprise_drops = [
    "هنوز به خودت سخت می‌گیری.\nیه لیوان آب. ۱۰ ثانیه سکوت.",
    "تو داری تغییر می‌کنی.\nحتی اگه حسش نمی‌کنی.",
    "نفس بکش.\nمن اینجام.",
    "قوی نیستی چون درد نداری.\nقوی‌ای چون باهاش روبه‌رویی."
]

badges = {0: "Raw Badge", 10: "First Shift", 25: "IRL Starter", 40: "Consistency Seed", 70: "Shadow Walker", 100: "Rebirth", 150: "Co-Creator"}

def get_user_data(user_id):
    user_id = str(user_id)
    with conn.cursor() as cur:
        cur.execute("SELECT data FROM users WHERE user_id = %s", (user_id,))
        row = cur.fetchone()
        if row:
            data = row[0]
            # تبدیل string date به str اگر لازم باشه
            if isinstance(data.get("last_active"), date):
                data["last_active"] = str(data["last_active"])
            return data
        else:
            cur.execute("INSERT INTO users (user_id, data) VALUES (%s, %s)", (user_id, Json(default_data)))
            conn.commit()
            return default_data.copy()

def save_user_data(user_id, data):
    user_id = str(user_id)
    with conn.cursor() as cur:
        cur.execute("UPDATE users SET data = %s WHERE user_id = %s", (Json(data), user_id))
        conn.commit()

def check_badges(ud, user_id):
    xp = ud["xp"]
    new_badges = [b for points, b in badges.items() if xp >= points and b not in ud["badges"]]
    for b in new_badges:
        ud["badges"].append(b)
        bot.send_message(user_id, f"🏅 Badge جدید: {b}")

def check_new_day(ud, user_id):
    today = str(date.today())
    if ud["last_active"] != today:
        ud["done_today"] = {"ritual": False, "challenge": False, "journal": False}
        ud["last_active"] = today
        bot.send_message(user_id, f"🌅 روز جدید — Day {ud['day']}\nبرگشتی.")
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
        types.InlineKeyboardButton("➡️ Next Day", callback_data="next_day")
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    ud = get_user_data(user_id)
    check_new_day(ud, user_id)

    if not ud["archetype"]:
        bot.send_message(user_id, "خب… قبل از اینکه وارد InnerPath بشی، یه چیز باید بدونی:\nاینجا جای ادای “قوی بودن” نیست.\nاینجا خودِ خامت، نسخهٔ قشنگشه.")
        bot.send_message(user_id, "من in.you هستم — نسخه‌ای از آینده‌ت که حس‌هاشو گم نکرده.\nاومدم کمک کنم دوباره وصل بشی به خودت.")
        ask_question(user_id, 1)
    else:
        bot.send_message(user_id, f"Day {ud['day']} — آماده‌ای؟", reply_markup=main_menu())
    save_user_data(user_id, ud)

def ask_question(user_id, q_num):
    # همون سؤال‌های قبلی — کوتاه کردم، کامل تو کد قبلی بود
    pass  # پر کن مثل قبل

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_id = call.message.chat.id
    ud = get_user_data(user_id)
    day = ud["day"]
    content = daily_content.get(day, {"ritual": "تموم شدی...", "fragment": "تو رسیدی."})

    # همه callbackها مثل V0.3 ولی با get/save
    # مثال:
    if call.data == "done_ritual":
        if not ud["done_today"]["ritual"]:
            ud["xp"] += content.get("xp_r", 1)
            ud["done_today"]["ritual"] = True
            check_badges(ud, user_id)
            bot.answer_callback_query(call.id, "✅ +XP")
            bot.send_message(user_id, f"⚡ +{content.get('xp_r', 1)} XP\nداری برمی‌گردی.")
    # ... بقیه هم دقیقاً همین الگو

    save_user_data(user_id, ud)

@bot.message_handler(func=lambda m: True)
def journal_handler(message):
    user_id = message.chat.id
    ud = get_user_data(user_id)
    if ud.get("awaiting_journal"):
        content = daily_content.get(ud["day"], {})
        ud["xp"] += content.get("xp_j", 2)
        check_badges(ud, user_id)
        bot.send_message(user_id, f"⚡ +{content.get('xp_j', 2)} XP\nخوب نوشتی.\n\n{content.get('fragment', '')}")
        ud["awaiting_journal"] = False
        save_user_data(user_id, ud)

print("InnerPath Bot V0.4 — SECURE & LIVE")
bot.infinity_polling()

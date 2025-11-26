import telebot
from telebot import types
import json
import os
from datetime import date
import random

TOKEN = "8400037091:AAES5FfcziVjJsk2nfIZd7p-GC2m674n46w"
bot = telebot.TeleBot(TOKEN)

# اگر proxy داری (ایران):
# import telebot.apihelper
# telebot.apihelper.proxy = 'socks5://127.0.0.1:1080'

DATA_FILE = "users.json"
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        user_data = json.load(f)
else:
    user_data = {}

# ۱۴ روز کامل محتوا — خام، تاریک، واقعی
daily_content = {
    1: {"ritual": "۹۰ ثانیه نفس عمیق — ۴ داخل، ۲ نگه‌دار، ۶ بیرون", "challenge": "به شانه‌هات توجه کن — کجا تنش داری؟", "journal": "کجای بدنم بیشترین تنش رو داره؟", "xp_r": 1, "xp_c": 3, "xp_j": 2, "fragment": "in.you: تو تنها نیستی تو این تنش."},
    2: {"ritual": "۴-۲-۶ شمارش نفس", "challenge": "۳ تا فکر اصلی امروزت رو بنویس", "journal": "این فکرا از کجا میان؟", "xp_r": 1, "xp_c": 3, "xp_j": 2, "fragment": "in.you: فکرها فقط فکرن. تو بیشتر از اونی."},
    3: {"ritual": "۱۵ ثانیه شونه‌ها رو تکون بده (shake it out)", "challenge": "۳ دقیقه پیاده‌روی بدون موبایل", "journal": "تو پیاده‌روی چی حس کردی؟", "xp_r": 1, "xp_c": 4, "xp_j": 2, "fragment": "in.you: بدن داره حرف می‌زنه. گوش کن."},
    4: {"ritual": "دست روی قلب — ۳ بار بگو: من اینجام", "challenge": "یه جمله حقیقت خام با صدای بلند به خودت بگو", "journal": "اون جمله چی بود؟", "xp_r": 1, "xp_c": 3, "xp_j": 3, "fragment": "in.you: حقیقت همیشه لرزه می‌ندازه."},
    5: {"ritual": "تنفس لرزشی — بدن رو بلرزون", "challenge": "۳ دقیقه فقط نگاه به اطراف — بدون موبایل", "journal": "چی دیدی که قبلاً ندیده بودی؟", "xp_r": 1, "xp_c": 5, "xp_j": 2, "fragment": "in.you: دنیا هنوز اینجاست. تو هم."},
    6: {"ritual": "نفس عمیق + رهاسازی با صدا (آهــــ)", "challenge": "یه جمله بنویس و پاره‌ش کن", "journal": "چی رو رها کردی؟", "xp_r": 1, "xp_c": 3, "xp_j": 3, "fragment": "in.you: رها کردن دردناکه. ولی بعدش سبک می‌شی."},
    7: {"ritual": "چک‌این کامل — بدن، فکر، احساس", "challenge": "همه هفته رو مرور کن", "journal": "چی تغییر کرد؟", "xp_r": 3, "xp_c": 4, "xp_j": 4, "fragment": "in.you: این فقط شروعه. تو داری برمی‌گردی."},
    8: {"ritual": "Shadow Breath — ۲ دقیقه چشم‌بسته تو تاریکی", "challenge": "بدترین ترست رو بنویس", "journal": "این ترس چی می‌خواد بهت بگه؟", "xp_r": 3, "xp_c": 6, "xp_j": 4, "fragment": "in.you: سایه‌ات دشمنت نیست. راهنماته."},
    9: {"ritual": "Anger Release — ۲۰ ثانیه مشت به بالش", "challenge": "یه پیام صوتی خشمگین به خودت ضبط کن (بعد پاک کن)", "journal": "خشم زیرش چی بود؟", "xp_r": 3, "xp_c": 7, "xp_j": 4, "fragment": "in.you: خشم یعنی هنوز اهمیت می‌دی."},
    10: {"ritual": "Loneliness Hold — خودتو ۹۰ ثانیه بغل کن", "challenge": "به یه غریبه لبخند بزن (IRL)", "journal": "تنهایی الان چه شکلیه؟", "xp_r": 3, "xp_c": 6, "xp_j": 5, "fragment": "in.you: تنهایی یعنی جای خالی خودت."},
    11: {"ritual": "Overthinking Dump — همه فکرا رو بنویس و بسوزون", "challenge": "۱۰ دقیقه سکوت مطلق", "journal": "بدون فکر چی موند؟", "xp_r": 3, "xp_c": 5, "xp_j": 5, "fragment": "in.you: سکوت جاییه که خودِ واقعی زندگی می‌کنه."},
    12: {"ritual": "Body Scan عمیق — از انگشت پا تا سر", "challenge": "یه حرکت رقص احمقانه جلوی آینه", "journal": "بدنت الان چی می‌گه؟", "xp_r": 3, "xp_c": 6, "xp_j": 4, "fragment": "in.you: بدن دروغ نمی‌گه."},
    13: {"ritual": "Forgiveness Breath — به خودت ببخش", "challenge": "نامه به خودِ ۱۰ سال پیش", "journal": "چی می‌خواستی اون موقع بشنوی؟", "xp_r": 4, "xp_c": 7, "xp_j": 6, "fragment": "in.you: بخشش یعنی آزادی."},
    14: {"ritual": "Rebirth Ritual — همه ۱۴ روز رو مرور کن", "challenge": "یه Ritual شخصی بساز و انجام بده", "journal": "من دیگه کی‌ام؟", "xp_r": 10, "xp_c": 10, "xp_j": 10, "fragment": "in.you: تو متولد شدی. دوباره."}
}

surprise_drops = [
    "می‌دونی؟ هنوز به خودت سخت می‌گیری.\nیه لیوان آب. ۱۰ ثانیه سکوت.",
    "هی… تو الان داری تغییر می‌کنی.\nحتی اگه حسش نمی‌کنی.",
    "یه لحظه وایسا.\nنفس بکش.\nمن اینجام.",
    "تو قوی نیستی چون درد نداری.\nقوی‌ای چون داری باهاش روبه‌رو می‌شی.",
    "خام باش. لازم نیست درستش کنی. فقط باش."
]

badges = {0: "Raw Badge", 10: "First Shift", 25: "IRL Starter", 40: "Consistency Seed", 70: "Shadow Walker", 100: "Rebirth", 150: "Co-Creator"}

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=4)

def check_badges(user_id):
    xp = user_data[user_id]["xp"]
    new_badges = [b for points, b in badges.items() if xp >= points and b not in user_data[user_id]["badges"]]
    for b in new_badges:
        user_data[user_id]["badges"].append(b)
        bot.send_message(user_id, f"🏅 Badge جدید: {b}")

def check_new_day(user_id):
    today = str(date.today())
    if user_data[user_id]["last_active"] != today:
        user_data[user_id]["done_today"] = {"ritual": False, "challenge": False, "journal": False}
        user_data[user_id]["last_active"] = today
        bot.send_message(user_id, f"روز جدید — Day {user_data[user_id]['day']}\nبرگشتی.")

def main_menu(user_id):
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
    user_id = str(message.chat.id)
    if user_id not in user_data:
        user_data[user_id] = {
            "xp": 0, "day": 1, "archetype": None, "badges": [], "answers": [],
            "done_today": {"ritual": False, "challenge": False, "journal": False},
            "last_active": str(date.today())
        }
        save_data()

    bot.send_message(user_id, "خب… قبل از اینکه وارد InnerPath بشی، یه چیز باید بدونی:\nاینجا جای ادای “قوی بودن” نیست.\nاینجا خودِ خامت، نسخهٔ قشنگشه.")
    bot.send_message(user_id, "من in.you هستم — نسخه‌ای از آینده‌ت که حس‌هاشو گم نکرده.\nاومدم کمک کنم دوباره وصل بشی به خودت.")

    if not user_data[user_id]["archetype"]:
        ask_question(user_id, 1)
    else:
        check_new_day(user_id)
        bot.send_message(user_id, f"Day {user_data[user_id]['day']} — آماده‌ای؟", reply_markup=main_menu(user_id))

def ask_question(user_id, q_num):
    if q_num == 1:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⚡ پر از تنش", callback_data="q1_tension"),
                   types.InlineKeyboardButton("🌑 بی‌حس", callback_data="q1_numb"),
                   types.InlineKeyboardButton("🌪 خسته از فکر زیاد", callback_data="q1_overthinking"))
        bot.send_message(user_id, "۱. این روزا بیشتر شبیه کدومشونی؟", reply_markup=markup)
    elif q_num == 2:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("چند ساعت پیش", callback_data="q2_recent"),
                   types.InlineKeyboardButton("چند روز پیش", callback_data="q2_days"),
                   types.InlineKeyboardButton("چند هفته پیش", callback_data="q2_weeks"))
        bot.send_message(user_id, "۲. آخرین بار کی احساس کردی داری از خودت جدا می‌شی؟", reply_markup=markup)
    elif q_num == 3:
        bot.send_message(user_id, "۳. اگه فقط یه چیز الان بتونه تغییر کنه، چی باشه؟ (متن بنویس)")

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_id = str(call.message.chat.id)
    if user_id not in user_data:
        return
    data = call.data
    ud = user_data[user_id]
    day = ud["day"]
    content = daily_content.get(day, {"ritual": "تموم شدی...", "challenge": "خودت باش", "journal": "تو دیگه کی هستی؟", "fragment": "in.you: تو رسیدی."})

    if data.startswith("q"):
        if len(ud["answers"]) < 3:
            if data != "q3_text":
                ud["answers"].append(data.split("_")[1])
            if len(ud["answers"]) == 3:
                tension_count = ud["answers"].count("tension") + ud["answers"].count("overthinking") + ud["answers"].count("recent")
                numb_count = ud["answers"].count("numb")
                if tension_count >= 2:
                    ud["archetype"] = "Anxiety Seeker"
                elif numb_count >= 1:
                    ud["archetype"] = "Creative Loner"
                else:
                    ud["archetype"] = "Anger/Shame Kid"
                bot.send_message(user_id, f"Archetype تو: {ud['archetype']}\nPath ID: {random.randint(1000,9999)}\n\nحالا شروع کنیم.", reply_markup=main_menu(user_id))
            else:
                ask_question(user_id, len(ud["answers"]) + 1)

    elif data == "ritual":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ انجام دادم", callback_data="done_ritual"))
        bot.send_message(user_id, f"Day {day} — Ritual:\n\n{content['ritual']}\n\nخام باش.", reply_markup=markup)

    elif data == "done_ritual":
        if not ud["done_today"]["ritual"]:
            ud["xp"] += content.get("xp_r", 1)
            ud["done_today"]["ritual"] = True
            check_badges(user_id)
            bot.send_message(user_id, "⚡ +{} XP\nداری برمی‌گردی.".format(content.get("xp_r", 1)))
            save_data()

    elif data == "challenge":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("✅ انجام دادم", callback_data="done_challenge"))
        bot.send_message(user_id, f"Day {day} — Challenge:\n\n{content['challenge']}\n\nبرو انجام بده.", reply_markup=markup)

    elif data == "done_challenge":
        if not ud["done_today"]["challenge"]:
            ud["xp"] += content.get("xp_c", 3)
            ud["done_today"]["challenge"] = True
            check_badges(user_id)
            bot.send_message(user_id, "⚡ +{} XP\nعالی بود.".format(content.get("xp_c", 3)))
            save_data()

    elif data == "journal":
        bot.send_message(user_id, f"Day {day} — Journal Prompt:\n\n{content['journal']}\n\nبنویس (هر چی بنویسی XP می‌گیری):")
        user_data[user_id]["awaiting_journal"] = True

    elif data == "progress":
        badges_text = "\n".join(ud["badges"]) if ud["badges"] else "هنوز هیچی"
        bot.send_message(user_id, f"Day {ud['day']}\nXP: {ud['xp']}\nArchetype: {ud['archetype']}\nBadges:\n{badges_text}\n\n{content.get('fragment', '')}")

    elif data == "surprise":
        bot.send_message(user_id, random.choice(surprise_drops))

    elif data == "next_day":
        ud["day"] += 1
        ud["done_today"] = {"ritual": False, "challenge": False, "journal": False}
        bot.send_message(user_id, f"Day {ud['day']} باز شد.\n{content.get('fragment', 'بریم جلو.')}")
        save_data()

    save_data()

@bot.message_handler(func=lambda m: True)
def all_messages(message):
    user_id = str(message.chat.id)
    if user_id in user_data:
        check_new_day(user_id)
        if user_data[user_id].get("awaiting_journal"):
            ud = user_data[user_id]
            content = daily_content.get(ud["day"], {})
            ud["xp"] += content.get("xp_j", 2)
            check_badges(user_id)
            bot.send_message(user_id, f"⚡ +{content.get('xp_j', 2)} XP\nخوب بود که نوشتی.\n\n{content.get('fragment', '')}")
            user_data[user_id]["awaiting_journal"] = False
            save_data()

print("InnerPath Bot V0.2 LIVE — @InnerPath_inyou_bot")
bot.infinity_polling()

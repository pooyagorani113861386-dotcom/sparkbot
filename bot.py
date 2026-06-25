import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

TOKEN = "8989899101:AAHal_1AMWUikPJ-saP4-sG-vS-EPkzpQOs"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 🔒 کانال‌های اجباری
CHANNELS = [
    "@Spark_news_tel",
    "@Spark_rap",
    "@Spark_sport"
]

# 📦 آرشیو
ARCHIVE_CHANNEL = -1004336027245

# 🎬 کارتون‌ها (هر لینک = یک کد)
CARTOONS = {
    "ben10": {
        "title": "بن تن",
        "message_id": 2
    }
}

# 🧠 چک عضویت
async def is_member(user_id: int):
    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(ch, user_id)
            if member.status in ["left", "kicked"]:
                return False
        except:
            return False
    return True

# 📢 دکمه عضویت
def join_keyboard():
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="📢 کانال 1", url="https://t.me/Spark_news_tel")],
        [types.InlineKeyboardButton(text="🎤 کانال 2", url="https://t.me/Spark_rap")],
        [types.InlineKeyboardButton(text="⚽ کانال 3", url="https://t.me/Spark_sport")],
        [types.InlineKeyboardButton(text="🔄 بررسی عضویت", callback_data="check")]
    ])

# 📥 ارسال کارتون + حذف بعد 30 ثانیه
async def send_cartoon(user_id: int, code: str):
    data = CARTOONS[code]

    msg = await bot.copy_message(
        chat_id=user_id,
        from_chat_id=ARCHIVE_CHANNEL,
        message_id=data["message_id"]
    )

    notice = await bot.send_message(
        user_id,
        "⏳ این فایل بعد از 30 ثانیه حذف میشه"
    )

    await asyncio.sleep(30)

    try:
        await bot.delete_message(user_id, msg.message_id)
        await bot.delete_message(user_id, notice.message_id)
    except:
        pass

# 🚀 شروع (لینک دار)
@dp.message(CommandStart())
async def start(message: types.Message):
    args = message.text.split()
    code = args[1] if len(args) > 1 else None

    if not code or code not in CARTOONS:
        await message.answer("❌ لینک نامعتبره")
        return

    if not await is_member(message.from_user.id):
        await message.answer(
            "❗ برای دریافت کارتون باید عضو کانال‌ها باشی 👇",
            reply_markup=join_keyboard()
        )
        return

    # ✅ مستقیم ارسال بدون پیام اضافه
    await send_cartoon(message.from_user.id, code)

# 🔄 بررسی عضویت
@dp.callback_query(lambda c: c.data == "check")
async def check(call: types.CallbackQuery):

    if not await is_member(call.from_user.id):
        await call.answer("❌ هنوز عضو همه کانال‌ها نیستی", show_alert=True)
        return

    # ❗ بدون پیام اضافه → مستقیم ارسال
    await send_cartoon(call.from_user.id, "ben10")

# ▶️ اجرا
async def main():
    print("BOT RUNNING")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
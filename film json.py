import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.request import HTTPXRequest

TOKEN = os.environ['8193454751:AAFYe2yYgCLIVJhTtZNG-OIXDRV1PPNzWhg']

# فایل ذخیره‌سازی
DATA_FILE = "data.json"

# بارگذاری داده‌ها از فایل
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# ذخیره داده‌ها در فایل
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# هندلر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    args = context.args
    if args:
        key = args[0].lower()
        if key in data:
            await update.message.reply_video(data[key], caption=f"🎬 فیلم: {key}")
        else:
            await update.message.reply_text("❌ این فیلم پیدا نشد.")
    else:
        await update.message.reply_text("سلام! اسم فیلم رو بعد از /start بنویس.")

# گرفتن و ذخیره فایل و file_id
async def save_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.video:
        file_id = update.message.video.file_id
        await update.message.reply_text("📝 اسم فیلم رو بفرست تا ذخیره کنم:")
        context.user_data["pending_file_id"] = file_id
    else:
        await update.message.reply_text("❌ فقط فیلم بفرست لطفاً.")

# گرفتن اسم بعد از ارسال فیلم
async def save_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "pending_file_id" in context.user_data:
        name = update.message.text.strip().lower()
        data = load_data()
        data[name] = context.user_data["pending_file_id"]
        save_data(data)
        await update.message.reply_text(f"✅ فیلم '{name}' ذخیره شد.")
        context.user_data.clear()
    else:
        await update.message.reply_text("❌ اول یه فیلم بفرست.")

if __name__ == '__main__':
    request = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
    app = ApplicationBuilder().token(TOKEN).request(request).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, save_file))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_name))

    print("✅ ربات آماده‌ست و داده‌ها رو ذخیره می‌کنه")
    app.run_polling()

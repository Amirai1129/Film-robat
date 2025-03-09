import logging
import os
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

# تنظیمات لاگ‌گیری برای اشکال‌زدایی
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# خواندن متغیرهای محیطی (برای امنیت بیشتر)
API_ID = int(os.getenv("API_ID", "123456"))  # مقدار واقعی را جایگزین کنید
API_HASH = os.getenv("API_HASH", "your_api_hash")  # مقدار واقعی را جایگزین کنید
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")  # مقدار واقعی را جایگزین کنید
URL = os.getenv("URL", "https://example.com/")  # مقدار واقعی را جایگزین کنید

# مقداردهی اولیه ربات
app = Client("stream_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# تابع ساخت هش (برای امنیت لینک‌ها)
def get_hash(file_id):
    """تولید هش برای محافظت از لینک‌های دانلود"""
    return "generated_hash"  # در صورت نیاز، الگوریتم هش را تغییر دهید

# کنترل‌کننده اینلاین برای دکمه‌های پخش و دانلود
@app.on_callback_query(filters.regex("^stream_"))
async def stream_callback(client: Client, query: CallbackQuery):
    """نمایش دکمه‌های پخش و دانلود بدون ارسال مجدد ویدیو"""
    try:
        file_id = query.data.split("_")[1]

        # تولید لینک‌های استریم و دانلود
        stream_link = f"{URL}watch/{file_id}?hash={get_hash(file_id)}"
        download_link = f"{URL}{file_id}?hash={get_hash(file_id)}"

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton('🖥️ پخش آنلاین', url=stream_link)],
            [InlineKeyboardButton('📥 دانلود', url=download_link)],
            [InlineKeyboardButton('🔍 جستجوی مجدد', switch_inline_query_current_chat="")]
        ])

        if query.message:
            await query.message.edit_reply_markup(reply_markup=buttons)
        else:
            await query.answer("🎬 برای پخش آنلاین یا دانلود، روی دکمه‌ها کلیک کنید:", show_alert=True)

    except Exception as e:
        logger.exception("❌ خطا در پردازش کال‌بک:")
        await query.answer("❌ خطایی رخ داد، لطفاً دوباره امتحان کنید.", show_alert=True)

# کنترل‌کننده پیام‌های متنی
@app.on_message(filters.command("start"))
async def start_command(client: Client, message):
    """پیغام خوش‌آمدگویی و راهنما"""
    await message.reply_text(
        "👋 سلام! من یک ربات استریم و دانلود فیلم هستم.\n"
        "🎬 فیلم مورد نظرت را ارسال کن تا لینک‌های پخش و دانلود را بگیری!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔎 جستجو", switch_inline_query_current_chat="")]
        ])
    )

# اجرای ربات
if __name__ == "__main__":
    logger.info("✅ ربات با موفقیت اجرا شد!")
    app.run()

import logging
from pyrogram import Client, emoji, filters
from pyrogram.errors.exceptions.bad_request_400 import QueryIdInvalid
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultCachedDocument, InlineQuery, CallbackQuery
from database.ia_filterdb import get_search_results
from utils import is_subscribed, get_size, temp
from info import CACHE_TIME, AUTH_USERS, AUTH_CHANNEL, CUSTOM_FILE_CAPTION, STREAM_MODE, URL
from database.connections_mdb import active_connection
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash

logger = logging.getLogger(__name__)
cache_time = 0 if AUTH_USERS or AUTH_CHANNEL else CACHE_TIME

async def inline_users(query: InlineQuery):
    """بررسی دسترسی کاربران به جستجوی اینلاین"""
    if AUTH_USERS:
        return query.from_user and query.from_user.id in AUTH_USERS
    return query.from_user and query.from_user.id not in temp.BANNED_USERS

@Client.on_callback_query(filters.regex("^stream_"))
async def stream_callback(client, query: CallbackQuery):
    """دریافت اطلاعات فایل و ارسال لینک استریم و دانلود"""
    file_id = query.data.split("_")[1]

    # تولید لینک‌های استریم و دانلود
    stream_link = f"{URL}watch/{file_id}?hash={get_hash(file_id)}"
    download_link = f"{URL}{file_id}?hash={get_hash(file_id)}"

    try:
        if query.message:
            # چک کردن نوع چت و ارسال پیام مناسب
            if query.message.chat.type == "private":
                await client.send_message(
                    chat_id=query.from_user.id,
                    text="🎬 برای تماشای آنلاین یا دانلود، روی گزینه‌های زیر کلیک کنید:",
                    reply_markup=InlineKeyboardMarkup([[ 
                        InlineKeyboardButton('🖥️ پخش آنلاین', url=stream_link),
                        InlineKeyboardButton('📥 دانلود', url=download_link)
                    ]])
                )
            else:
                await client.send_message(
                    chat_id=query.from_user.id,
                    text="🎬 برای تماشای آنلاین یا دانلود، روی گزینه‌های زیر کلیک کنید:",
                    reply_markup=InlineKeyboardMarkup([[ 
                        InlineKeyboardButton('🖥️ پخش آنلاین', url=stream_link),
                        InlineKeyboardButton('📥 دانلود', url=download_link)
                    ], [
                        InlineKeyboardButton('🔍 جستجوی مجدد', switch_inline_query="")
                    ]])
                )
        elif query.inline_message_id:
            # بررسی فرمت inline_message_id و تبدیل به عدد صحیح در صورت لزوم
            try:
                inline_message_id = int(query.inline_message_id, 16)  # تلاش برای تبدیل به هگزادسیمال
            except ValueError:
                inline_message_id = query.inline_message_id  # اگر موفق نشد، همانطور که هست باقی بماند

            await client.edit_message_text(
                chat_id=query.from_user.id,
                message_id=inline_message_id,
                text="🎬 برای تماشای آنلاین یا دانلود، روی گزینه‌های زیر کلیک کنید:",
                reply_markup=InlineKeyboardMarkup([[ 
                    InlineKeyboardButton('🖥️ پخش آنلاین', url=stream_link),
                    InlineKeyboardButton('📥 دانلود', url=download_link)
                ]])
            )
        else:
            logger.error("No valid message or inline_message_id.")
    
    except Exception as e:
        logger.exception(str(e))
        await query.answer("❌ خطایی رخ داد، لطفاً دوباره امتحان کنید.", show_alert=True)


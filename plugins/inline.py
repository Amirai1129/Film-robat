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

@Client.on_inline_query()
async def answer(bot, query):
    """جستجوی اینلاین و نمایش فایل‌ها"""
    chat_id = await active_connection(str(query.from_user.id))
    
    if not await inline_users(query):
        await query.answer(
            results=[], cache_time=0,
            switch_pm_text='دسترسی شما محدود شده است!',
            switch_pm_parameter="access_denied"
        )
        return

    if AUTH_CHANNEL and not await is_subscribed(bot, query):
        await query.answer(
            results=[], cache_time=0,
            switch_pm_text='برای استفاده، عضو کانال شوید!',
            switch_pm_parameter="subscribe"
        )
        return

    results = []
    query_text = query.query.strip()
    file_type = None

    if '|' in query_text:
        query_text, file_type = map(str.strip, query_text.split('|', maxsplit=1))
        file_type = file_type.lower()

    offset = int(query.offset or 0)
    files, next_offset, total = await get_search_results(chat_id, query_text, file_type=file_type, max_results=10, offset=offset)

    for file in files:
        title = file['file_name']
        size = get_size(file['file_size'])
        caption = file.get('caption', title)
        file_id = file['file_id']

        # ایجاد دکمه کال‌بک برای ارسال استریم و دانلود
        buttons = InlineKeyboardMarkup([[ 
            InlineKeyboardButton("🎥 ساخت لینک دانلود مستقیم", callback_data=f"stream_{file_id}")
        ]])

        # افزودن نتیجه به لیست
        results.append(
            InlineQueryResultCachedDocument(
                title=title,
                document_file_id=file_id,
                caption=caption,
                description=f'حجم فایل: {size}',
                reply_markup=buttons
            )
        )

    # نمایش نتایج جستجو
    switch_pm_text = f"{emoji.FILE_FOLDER} تعداد نتایج: {total}"
    if query_text:
        switch_pm_text += f" برای '{query_text}'"

    try:
        await query.answer(
            results=results,
            is_personal=True,
            cache_time=cache_time,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter="start",
            next_offset=str(next_offset)
        )
    except QueryIdInvalid:
        pass
    except Exception as e:
        logger.exception(str(e))


@Client.on_callback_query(filters.regex("^stream_"))
async def stream_callback(client, query: CallbackQuery):
    """دریافت اطلاعات فایل و ارسال لینک استریم و دانلود"""
    file_id = query.data.split("_")[1]

    # تولید لینک‌های استریم و دانلود
    stream_link = f"{URL}watch/{file_id}?hash={get_hash(file_id)}"
    download_link = f"{URL}{file_id}?hash={get_hash(file_id)}"

    try:
        # چک کردن نوع فایل و ارسال مناسب
        if query.message.chat.type == "private":
            # اگر کاربر در چت خصوصی است، ارسال دکمه‌ها در همان چت خصوصی
            await client.send_message(
                chat_id=query.from_user.id,
                text="🎬 برای تماشای آنلاین یا دانلود، روی گزینه‌های زیر کلیک کنید:",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton('🖥️ پخش آنلاین', url=stream_link),
                    InlineKeyboardButton('📥 دانلود', url=download_link)
                ], [
                    InlineKeyboardButton('🔍 جستجوی مجدد', switch_inline_query_current_chat="")
                ]])
            )
        else:
            # اگر کاربر در یک گروه است، هدایت به ربات
            await client.send_message(
                chat_id=query.from_user.id,
                text="🎬 برای تماشای آنلاین یا دانلود، روی گزینه‌های زیر کلیک کنید:",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton('🖥️ پخش آنلاین', url=stream_link),
                    InlineKeyboardButton('📥 دانلود', url=download_link)
                ], [
                    InlineKeyboardButton('🔍 جستجوی مجدد', switch_inline_query="")  # هدایت به ربات
                ]])
            )
    
    except Exception as e:
        logger.exception(str(e))
        await query.answer("❌ خطایی رخ داد، لطفاً دوباره امتحان کنید.", show_alert=True)

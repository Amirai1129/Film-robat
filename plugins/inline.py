import logging
import aiohttp
import uuid
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    InlineQueryResultArticle, InputTextMessageContent, CallbackQuery
)
from database.ia_filterdb import get_search_results
from utils import get_size
from info import CACHE_TIME, AUTH_USERS, AUTH_CHANNEL, URL
from database.connections_mdb import active_connection
from TechVJ.util.file_properties import get_hash

# 🔹 تنظیمات لاگ‌گیری برای اشکال‌زدایی
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

cache_time = 0 if AUTH_USERS or AUTH_CHANNEL else CACHE_TIME

# 🔹 کلید API برای دریافت اطلاعات IMDb از OMDb API
OMDB_API_KEY = "ae759efb"


async def get_movie_info(title):
    """📌 دریافت اطلاعات فیلم از IMDb با استفاده از OMDb API"""
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data.get("Response") == "True":
                    return {
                        "title": data.get("Title"),
                        "year": data.get("Year"),
                        "rating": data.get("imdbRating"),
                        "genre": data.get("Genre"),
                        "poster": data.get("Poster"),
                        "plot": data.get("Plot"),
                        "imdb_link": f"https://www.imdb.com/title/{data.get('imdbID')}/",
                        "trailer": f"https://www.youtube.com/results?search_query={title.replace(' ', '+')}+trailer"
                    }
    return None  # ❌ در صورت یافت نشدن اطلاعات


@Client.on_inline_query()
async def answer(bot, query):
    """🔍 جستجوی اینلاین + نمایش اطلاعات IMDb و دکمه‌های اختصاصی"""
    chat_id = await active_connection(str(query.from_user.id))
    search_text = query.query.strip()

    if not search_text:
        await query.answer([], cache_time=0)
        return

    # 📌 دریافت اطلاعات فیلم از IMDb
    movie_info = await get_movie_info(search_text)
    if not movie_info:
        logger.warning(f"⚠️ اطلاعاتی برای '{search_text}' یافت نشد.")
        await query.answer([], cache_time=0, switch_pm_text="❌ فیلمی یافت نشد!")
        return

    # 📌 دکمه‌های اکشن برای فیلم
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎥 نمایش فایل‌های مرتبط", callback_data=f"show_files_{search_text}")],
        [InlineKeyboardButton("📺 تماشای تریلر", url=movie_info['trailer']),
         InlineKeyboardButton("ℹ️ اطلاعات IMDb", url=movie_info['imdb_link'])],
        [InlineKeyboardButton("🔍 جستجوی مجدد", switch_inline_query="")]
    ])

    # 📌 نمایش نتایج اینلاین
    results = [
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title=f"{movie_info['title']} ({movie_info['year']})",
            description=f"⭐️ امتیاز IMDb: {movie_info['rating']} | 🎭 ژانر: {movie_info['genre']}",
            thumb_url=movie_info['poster'],
            input_message_content=InputTextMessageContent(
                message_text=f"🎬 *{movie_info['title']}* ({movie_info['year']})\n\n"
                             f"⭐️ *امتیاز:* {movie_info['rating']}\n"
                             f"🎭 *ژانر:* {movie_info['genre']}\n"
                             f"📜 *داستان:* {movie_info['plot']}\n\n"
                             f"[📸 کاور]({movie_info['poster']})",
                parse_mode="markdown",
                disable_web_page_preview=False
            ),
            reply_markup=buttons
        )
    ]

    await query.answer(results, is_personal=True, cache_time=cache_time)


@Client.on_callback_query(filters.regex("^show_files_"))
async def show_files(client, query: CallbackQuery):
    """📂 نمایش فایل‌های مرتبط با فیلم جستجو شده"""
    movie_title = query.data.split("_", 2)[2]
    chat_id = await active_connection(str(query.from_user.id))

    # 📌 دریافت فایل‌های مرتبط از دیتابیس
    files, _, _ = await get_search_results(chat_id, movie_title, max_results=10)

    if not files:
        await query.answer("❌ هیچ فایلی برای این فیلم یافت نشد!", show_alert=True)
        return

    for file in files:
        title = file['file_name']
        size = get_size(file['file_size'])
        file_id = file['file_id']

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎥 پخش آنلاین", callback_data=f"stream_{file_id}"),
             InlineKeyboardButton("📥 دانلود", callback_data=f"download_{file_id}")]
        ])

        await client.send_document(
            chat_id=query.from_user.id,
            document=file_id,
            caption=f"🎬 {title}\nحجم: {size}",
            reply_markup=buttons
        )

    await query.answer()


@Client.on_callback_query(filters.regex("^stream_"))
async def stream_callback(client, query: CallbackQuery):
    """🔗 ارسال لینک‌های پخش آنلاین و دانلود"""
    file_id = query.data.split("_")[1]
    stream_link = f"{URL}watch/{file_id}?hash={get_hash(file_id)}"
    download_link = f"{URL}{file_id}?hash={get_hash(file_id)}"

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton('🖥️ پخش آنلاین', url=stream_link),
         InlineKeyboardButton('📥 دانلود', url=download_link)],
        [InlineKeyboardButton('🔍 جستجوی مجدد', switch_inline_query="")]
    ])

    await client.send_message(
        chat_id=query.from_user.id,
        text="🎬 برای تماشای آنلاین یا دانلود، روی گزینه‌های زیر کلیک کنید:",
        reply_markup=buttons
    )
    await query.answer()

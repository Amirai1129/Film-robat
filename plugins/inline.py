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

# 🔹 کلید API برای دریافت اطلاعات فیلم از TMDb API
TMDB_API_KEY = "49b9a0708b541637a7738f9adc4a4417"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

async def get_movie_info(title):
    """📌 دریافت اطلاعات فیلم از TMDb API
    """
    url = f"{TMDB_BASE_URL}/search/movie?api_key={TMDB_API_KEY}&query={title}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                results = data.get("results", [])
                if results:
                    movie = results[0]
                    movie_id = movie.get("id")
                    details_url = f"{TMDB_BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}"
                    async with session.get(details_url) as details_response:
                        details = await details_response.json()
                        return {
                            "title": details.get("title"),
                            "year": details.get("release_date", "Unknown").split("-")[0],
                            "rating": details.get("vote_average", "N/A"),
                            "genre": ", ".join([g["name"] for g in details.get("genres", [])]),
                            "poster": f"https://image.tmdb.org/t/p/w500{details.get('poster_path')}",
                            "plot": details.get("overview"),
                            "imdb_link": f"https://www.imdb.com/title/{details.get('imdb_id')}/",
                            "trailer": f"https://www.youtube.com/results?search_query={title.replace(' ', '+')}+trailer"
                        }
    return None  # ❌ در صورت یافت نشدن اطلاعات


@Client.on_inline_query()
async def answer(bot, query):
    """🔍 جستجوی اینلاین + نمایش اطلاعات TMDb و دکمه‌های اختصاصی
    """
    chat_id = await active_connection(str(query.from_user.id))
    search_text = query.query.strip()

    if not search_text:
        await query.answer([], cache_time=0)
        return

    movie_info = await get_movie_info(search_text)
    if not movie_info:
        logger.warning(f"⚠️ اطلاعاتی برای '{search_text}' یافت نشد.")
        await query.answer([], cache_time=0, switch_pm_text="❌ فیلمی یافت نشد!")
        return

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎥 نمایش فایل‌های مرتبط", callback_data=f"show_files_{search_text}")],
        [InlineKeyboardButton("📺 تماشای تریلر", url=movie_info['trailer']),
         InlineKeyboardButton("ℹ️ اطلاعات IMDb", url=movie_info['imdb_link'])],
        [InlineKeyboardButton("🔍 جستجوی مجدد", switch_inline_query="")]
    ])

    results = [
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title=f"{movie_info['title']} ({movie_info['year']})",
            description=f"⭐️ امتیاز TMDb: {movie_info['rating']} | 🎭 ژانر: {movie_info['genre']}",
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

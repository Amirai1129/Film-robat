from pyrogram import client, filters

@Client.on_callback_query(filters.regex("^stream_"))
async def stream_callback(client, query: CallbackQuery):
    """ارسال دکمه‌های پخش و دانلود بدون ارسال مجدد ویدیو"""
    file_id = query.data.split("_")[1]

    # تولید لینک‌های استریم و دانلود
    stream_link = f"{URL}watch/{file_id}?hash={get_hash(file_id)}"
    download_link = f"{URL}{file_id}?hash={get_hash(file_id)}"

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton('🖥️ پخش آنلاین', url=stream_link)],
        [InlineKeyboardButton('📥 دانلود', url=download_link)],
        [InlineKeyboardButton('🔍 جستجوی مجدد', switch_inline_query_current_chat="")]
    ])

    try:
        if query.message:
            # ویرایش پیام و اضافه کردن دکمه‌های جدید
            await query.message.edit_reply_markup(reply_markup=buttons)
        else:
            # اگر پیام وجود نداشت، دکمه‌ها را از طریق query.answer ارسال می‌کنیم
            await query.answer("🎬 برای پخش آنلاین یا دانلود، روی دکمه‌ها کلیک کنید:", show_alert=True)
    except Exception as e:
        logger.exception(str(e))
        await query.answer("❌ خطایی رخ داد، لطفاً دوباره امتحان کنید.", show_alert=True)

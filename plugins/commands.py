# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os, string, logging, random, asyncio, time, datetime, re, sys, json, base64
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import *
from database.ia_filterdb import col, sec_col, get_file_details, unpack_new_file_id, get_bad_files
from database.users_chats_db import db, delete_all_referal_users, get_referal_users_count, get_referal_all_users, referal_add_user
from database.join_reqs import JoinReqs
from info import CLONE_MODE, OWNER_LNK, REACTIONS, CHANNELS, REQUEST_TO_JOIN_MODE, TRY_AGAIN_BTN, ADMINS, SHORTLINK_MODE, PREMIUM_AND_REFERAL_MODE, STREAM_MODE, AUTH_CHANNEL, REFERAL_PREMEIUM_TIME, REFERAL_COUNT, PAYMENT_TEXT, PAYMENT_QR, LOG_CHANNEL, PICS, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, PROTECT_CONTENT, CHNL_LNK, GRP_LNK, REQST_CHANNEL, SUPPORT_CHAT, MAX_B_TN, VERIFY, SHORTLINK_API, SHORTLINK_URL, TUTORIAL, VERIFY_TUTORIAL, IS_TUTORIAL, URL
from utils import get_settings, pub_is_subscribed, get_size, is_subscribed, save_group_settings, temp, verify_user, check_token, check_verification, get_token, get_shortlink, get_tutorial, get_seconds
from database.connections_mdb import active_connection
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
logger = logging.getLogger(__name__)

BATCH_FILES = {}
join_db = JoinReqs

from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
import random

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    try:
        await message.react(emoji=random.choice(REACTIONS), big=True)
    except:
        pass
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        buttons = [[
            InlineKeyboardButton('⤬ اضافه کردن من به گروه شما ⤬', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
        ],[
            InlineKeyboardButton('گروه پشتیبانی', url=f'https://t.me/{SUPPORT_CHAT}'),
            InlineKeyboardButton('گروه فیلم', url=GRP_LNK)
        ],[
            InlineKeyboardButton('عضویت در کانال اطلاع‌رسانی', url=CHNL_LNK)
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply(script.START_TXT.format(message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME), reply_markup=reply_markup, disable_web_page_preview=True)
        await asyncio.sleep(2)  # کمی صبر کن قبل از بررسی
        if not await db.get_chat(message.chat.id):
            total = await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "نامشخص"))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 

    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))

    if len(message.command) != 2:
        if PREMIUM_AND_REFERAL_MODE == True:
            buttons = [[
                InlineKeyboardButton('⤬ اضافه کردن من به گروه شما ⤬', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
            ],[
                InlineKeyboardButton('کسب درآمد', callback_data="shortlink_info"),
                InlineKeyboardButton('گروه فیلم', url=GRP_LNK)
            ],[
                InlineKeyboardButton('راهنما', callback_data='help'),
                InlineKeyboardButton('درباره', callback_data='about')
            ],[
                InlineKeyboardButton('اشتراک ویژه و معرفی به دوستان', callback_data='subscription')
            ],[
                InlineKeyboardButton('عضویت در کانال اطلاع‌رسانی', url=CHNL_LNK)
            ]]
        else:
            buttons = [[
                InlineKeyboardButton('⤬ اضافه کردن من به گروه شما ⤬', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
            ],[
                InlineKeyboardButton('کسب درآمد', callback_data="shortlink_info"),
                InlineKeyboardButton('گروه فیلم', url=GRP_LNK)
            ],[
                InlineKeyboardButton('راهنما', callback_data='help'),
                InlineKeyboardButton('درباره', callback_data='about')
            ],[
                InlineKeyboardButton('عضویت در کانال اطلاع‌رسانی', url=CHNL_LNK)
            ]]
        if CLONE_MODE == True:
            buttons.append([InlineKeyboardButton('ساخت ربات مشابه شخصی', callback_data='clone')])

        reply_markup = InlineKeyboardMarkup(buttons)
        m = await message.reply_sticker("CAACAgUAAxkBAAEKVaxlCWGs1Ri6ti45xliLiUeweCnu4AACBAADwSQxMYnlHW4Ls8gQMAQ") 
        await asyncio.sleep(1)
        await m.delete()
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
    
    if AUTH_CHANNEL and not await is_subscribed(client, message):
    try:
        if REQUEST_TO_JOIN_MODE == True:
            invite_link = await client.create_chat_invite_link(chat_id=(int(AUTH_CHANNEL)), creates_join_request=True)
        else:
            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
    except Exception as e:
        print(e)
        await message.reply_text("مطمئن شوید که ربات در کانال عضویت اجباری ادمین است.")
        return

    try:
        btn = [[InlineKeyboardButton("📢 کانال پشتیبان", url=invite_link.invite_link)]]
        if message.command[1] != "subscribe":
            if REQUEST_TO_JOIN_MODE == True:
                if TRY_AGAIN_BTN == True:
                    try:
                        kk, file_id = message.command[1].split("_", 1)
                        btn.append([InlineKeyboardButton("↻ تلاش مجدد", callback_data=f"checksub#{kk}#{file_id}")])
                    except (IndexError, ValueError):
                        btn.append([InlineKeyboardButton("↻ تلاش مجدد", url=f"https://t.me/{temp.U_NAME}?start={message.command[1]}")])
            else:
                try:
                    kk, file_id = message.command[1].split("_", 1)
                    btn.append([InlineKeyboardButton("↻ تلاش مجدد", callback_data=f"checksub#{kk}#{file_id}")])
                except (IndexError, ValueError):
                    btn.append([InlineKeyboardButton("↻ تلاش مجدد", url=f"https://t.me/{temp.U_NAME}?start={message.command[1]}")])

        if REQUEST_TO_JOIN_MODE == True:
            if TRY_AGAIN_BTN == True:
                text = "**🕵️ ابتدا به کانال پشتیبان من بپیوندید، سپس دوباره تلاش کنید.**"
            else:
                await db.set_msg_command(message.from_user.id, com=message.command[1])
                text = "**🕵️ ابتدا به کانال پشتیبان من بپیوندید.**"
        else:
            text = "**🕵️ ابتدا به کانال پشتیبان من بپیوندید، سپس دوباره تلاش کنید.**"

        await client.send_message(
            chat_id=message.from_user.id,
            text=text,
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    except Exception as e:
        print(e)
        return await message.reply_text("مشکلی در بررسی عضویت اجباری پیش آمده است.")

if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help"]:
    if PREMIUM_AND_REFERAL_MODE == True:
        buttons = [[
            InlineKeyboardButton('⤬ اضافه کردن من به گروه شما ⤬', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
        ],[
            InlineKeyboardButton('💰 کسب درآمد', callback_data="shortlink_info"),
            InlineKeyboardButton('🎬 گروه فیلم', url=GRP_LNK)
        ],[
            InlineKeyboardButton('📖 راهنما', callback_data='help'),
            InlineKeyboardButton('ℹ️ درباره', callback_data='about')
        ],[
            InlineKeyboardButton('⭐ اشتراک ویژه و معرفی به دوستان', callback_data='subscription')
        ],[
            InlineKeyboardButton('📢 عضویت در کانال اطلاع‌رسانی', url=CHNL_LNK)
        ]]
    else:
        buttons = [[
            InlineKeyboardButton('⤬ اضافه کردن من به گروه شما ⤬', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
        ],[
            InlineKeyboardButton('💰 کسب درآمد', callback_data="shortlink_info"),
            InlineKeyboardButton('🎬 گروه فیلم', url=GRP_LNK)
        ],[
            InlineKeyboardButton('📖 راهنما', callback_data='help'),
            InlineKeyboardButton('ℹ️ درباره', callback_data='about')
        ],[
            InlineKeyboardButton('📢 عضویت در کانال اطلاع‌رسانی', url=CHNL_LNK)
        ]]
    if CLONE_MODE == True:
        buttons.append([InlineKeyboardButton('🤖 ساخت ربات مشابه شخصی', callback_data='clone')])

    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_photo(
        photo=random.choice(PICS),
        caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML
    )
    return
    data = message.command[1]
if data.split("-", 1)[0] == "VJ":
    user_id = int(data.split("-", 1)[1])
    vj = await referal_add_user(user_id, message.from_user.id)
    if vj and PREMIUM_AND_REFERAL_MODE == True:
        await message.reply(f"<b>شما از طریق لینک معرفی کاربری با شناسه {user_id} وارد شده‌اید.\n\nلطفاً دوباره /start را ارسال کنید تا از ربات استفاده کنید.</b>")
        num_referrals = await get_referal_users_count(user_id)
        await client.send_message(
            chat_id=user_id,
            text=f"<b>{message.from_user.mention} از طریق لینک معرفی شما ربات را شروع کرد.\n\nتعداد کل معرفی‌ها: {num_referrals}</b>"
        )
        if num_referrals == REFERAL_COUNT:
            time = REFERAL_PREMEIUM_TIME       
            seconds = await get_seconds(time)
            if seconds > 0:
                expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
                user_data = {"id": user_id, "expiry_time": expiry_time} 
                await db.update_user(user_data)  
                await delete_all_referal_users(user_id)
                await client.send_message(
                    chat_id=user_id,
                    text=f"<b>شما با موفقیت تعداد لازم معرفی را تکمیل کردید.\n\nاکنون برای مدت {REFERAL_PREMEIUM_TIME} در حالت پریمیوم قرار گرفتید.</b>"
                )
                return 
    else:
        if PREMIUM_AND_REFERAL_MODE == True:
            buttons = [[
                InlineKeyboardButton('⤬ اضافه کردن من به گروه شما ⤬', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
            ],[
                InlineKeyboardButton('💰 کسب درآمد', callback_data="shortlink_info"),
                InlineKeyboardButton('🎬 گروه فیلم', url=GRP_LNK)
            ],[
                InlineKeyboardButton('📖 راهنما', callback_data='help'),
                InlineKeyboardButton('ℹ️ درباره', callback_data='about')
            ],[
                InlineKeyboardButton('⭐ اشتراک ویژه و معرفی', callback_data='subscription')
            ],[
                InlineKeyboardButton('📢 عضویت در کانال اطلاع‌رسانی', url=CHNL_LNK)
            ]]
        else:
            buttons = [[
                InlineKeyboardButton('⤬ اضافه کردن من به گروه شما ⤬', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
            ],[
                InlineKeyboardButton('💰 کسب درآمد', callback_data="shortlink_info"),
                InlineKeyboardButton('🎬 گروه فیلم', url=GRP_LNK)
            ],[
                InlineKeyboardButton('📖 راهنما', callback_data='help'),
                InlineKeyboardButton('ℹ️ درباره', callback_data='about')
            ],[
                InlineKeyboardButton('📢 عضویت در کانال اطلاع‌رسانی', url=CHNL_LNK)
            ]]

        if CLONE_MODE == True:
            buttons.append([InlineKeyboardButton('🤖 ساخت ربات مشابه شخصی', callback_data='clone')])

        reply_markup = InlineKeyboardMarkup(buttons)
        m = await message.reply_sticker("CAACAgUAAxkBAAEKVaxlCWGs1Ri6ti45xliLiUeweCnu4AACBAADwSQxMYnlHW4Ls8gQMAQ") 
        await asyncio.sleep(1)
        await m.delete()
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return 

try:
    pre, file_id = data.split('_', 1)
except:
    file_id = data
    pre = ""

if data.split("-", 1)[0] == "BATCH":
    sts = await message.reply("<b>لطفاً منتظر بمانید...</b>")
    file_id = data.split("-", 1)[1]
    msgs = BATCH_FILES.get(file_id)

    if not msgs:
        file = await client.download_media(file_id)
        try: 
            with open(file) as file_data:
                msgs = json.loads(file_data.read())
        except:
            await sts.edit("ناموفق ❌")
            return await client.send_message(LOG_CHANNEL, "خطا در باز کردن فایل.")

        os.remove(file)
        BATCH_FILES[file_id] = msgs

    filesarr = []
    for msg in msgs:
        title = msg.get("title")
        size = get_size(int(msg.get("size", 0)))
        f_caption = msg.get("caption", "")

        if BATCH_FILE_CAPTION:
            try:
                f_caption = BATCH_FILE_CAPTION.format(
                    file_name='' if title is None else title, 
                    file_size='' if size is None else size, 
                    file_caption='' if f_caption is None else f_caption
                )
            except:
                f_caption = f_caption

        if f_caption is None:
            f_caption = f"{title}"

        try:
            if STREAM_MODE == True:
                log_msg = await client.send_cached_media(chat_id=LOG_CHANNEL, file_id=msg.get("file_id"))
                fileName = {quote_plus(get_name(log_msg))}
                stream = f"{URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
                download = f"{URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"

            if STREAM_MODE == True:
                button = [[
                    InlineKeyboardButton("📥 دانلود", url=download),
                    InlineKeyboardButton('▶ تماشا', url=stream)
                ],[
                    InlineKeyboardButton("📺 تماشا در وب اپ", web_app=WebAppInfo(url=stream))
                ]]
                reply_markup = InlineKeyboardMarkup(button)
            else:
                reply_markup = None
                    
                msg = await client.send_cached_media(
    chat_id=message.from_user.id,
    file_id=msg.get("file_id"),
    caption=f_caption,
    protect_content=msg.get('protect', False),
    reply_markup=reply_markup
)
filesarr.append(msg)

# اگر ربات با محدودیت ارسال پیام مواجه شد، صبر کند و دوباره ارسال کند
try:
    pass
except FloodWait as e:
    await asyncio.sleep(e.value)
    msg = await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=msg.get("file_id"),
        caption=f_caption,
        protect_content=msg.get('protect', False),
        reply_markup=InlineKeyboardMarkup(button)
    )
    filesarr.append(msg)
except:
    continue

await asyncio.sleep(1) 
await sts.delete()

# ارسال پیام هشدار برای حذف خودکار پیام
k = await client.send_message(
    chat_id=message.from_user.id,
    text=f"<blockquote><b><u>❗️❗️❗️ مهم ❗️❗️❗️</u></b>\n\nاین پیام در <b><u>10 دقیقه</u> 🫥</b> حذف خواهد شد. "
         "<i>(به دلیل مسائل مربوط به کپی‌رایت)</i>.\n\n"
         "<b><i>لطفاً این پیام را به پیام‌های ذخیره‌شده یا یک چت خصوصی فوروارد کنید.</i></b></blockquote>"
)
await asyncio.sleep(600)

# حذف فایل‌ها پس از 10 دقیقه
for x in filesarr:
    await x.delete()

await k.edit_text("<b>✅ پیام شما با موفقیت حذف شد</b>")
return

elif data.split("-", 1)[0] == "DSTORE":
    sts = await message.reply("<b>لطفاً منتظر بمانید...</b>")
    b_string = data.split("-", 1)[1]
    decoded = (base64.urlsafe_b64decode(b_string + "=" * (-len(b_string) % 4))).decode("ascii")
    
    try:
        f_msg_id, l_msg_id, f_chat_id, protect = decoded.split("_", 3)
    except:
        f_msg_id, l_msg_id, f_chat_id = decoded.split("_", 2)
        protect = "/pbatch" if PROTECT_CONTENT else "batch"

    diff = int(l_msg_id) - int(f_msg_id)
    filesarr = []

    async for msg in client.iter_messages(int(f_chat_id), int(l_msg_id), int(f_msg_id)):
        if msg.media:
            media = getattr(msg, msg.media.value)
            file_type = msg.media
            file = getattr(msg, file_type.value)
            size = get_size(int(file.file_size))
            file_name = getattr(media, 'file_name', '')
            f_caption = getattr(msg, 'caption', file_name)

            if BATCH_FILE_CAPTION:
                try:
                    f_caption = BATCH_FILE_CAPTION.format(
                        file_name=file_name, 
                        file_size='' if size is None else size, 
                        file_caption=f_caption
                    )
                except:
                    f_caption = getattr(msg, 'caption', '')

            file_id = file.file_id

            if STREAM_MODE:
                log_msg = await client.send_cached_media(chat_id=LOG_CHANNEL, file_id=file_id)
                fileName = {quote_plus(get_name(log_msg))}
                stream = f"{URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
                download = f"{URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"

            if STREAM_MODE:
                button = [[
                    InlineKeyboardButton("📥 دانلود", url=download),
                    InlineKeyboardButton('▶ تماشا', url=stream)
                ],[
                    InlineKeyboardButton("📺 تماشا در وب اپ", web_app=WebAppInfo(url=stream))
                ]]
                reply_markup = InlineKeyboardMarkup(button)
            else:
                reply_markup = None

            try:
                p = await msg.copy(
                    message.chat.id, 
                    caption=f_caption, 
                    protect_content=True if protect == "/pbatch" else False, 
                    reply_markup=reply_markup
                )
            except FloodWait as e:
                await asyncio.sleep(e.value)
                p = await msg.copy(
                    message.chat.id, 
                    caption=f_caption, 
                    protect_content=True if protect == "/pbatch" else False, 
                    reply_markup=reply_markup
                )
            except:
                continue
        elif msg.empty:
            continue
        else:
            try:
                p = await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                p = await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
            except:
                continue

        filesarr.append(p)
        await asyncio.sleep(1)

    await sts.delete()
    k = await client.send_message(
        chat_id=message.from_user.id, 
        text=f"<blockquote><b><u>❗️❗️❗️ مهم ❗️❗️❗️</u></b>\n\nاین پیام در <b><u>10 دقیقه</u> 🫥</b> حذف خواهد شد. "
             "<i>(به دلیل مسائل مربوط به کپی‌رایت)</i>.\n\n"
             "<b><i>لطفاً این پیام را به پیام‌های ذخیره‌شده یا یک چت خصوصی فوروارد کنید.</i></b></blockquote>"
    )
    await asyncio.sleep(600)

    for x in filesarr:
        await x.delete()

    await k.edit_text("<b>✅ پیام شما با موفقیت حذف شد</b>")
    return
    elif data.split("-", 1)[0] == "verify":
    userid = data.split("-", 2)[1]
    token = data.split("-", 3)[2]
    if str(message.from_user.id) != str(userid):
        return await message.reply_text(text="<b>لینک نامعتبر یا لینک منقضی شده است</b>", protect_content=True)
    is_valid = await check_token(client, userid, token)
    if is_valid == True:
        text = "<b>سلام {} 👋,\n\nشما تایید اعتبار را تکمیل کرده‌اید...\n\nحالا شما دسترسی نامحدود دارید تا امروز، حالا از آن لذت ببرید\n\n</b>"
        if PREMIUM_AND_REFERAL_MODE == True:
            text += "<b>اگر می‌خواهید فایل‌های مستقیم بدون هیچ تاییدیه‌ای خریداری کنید، اشتراک ربات را بخرید ☺️\n\n💶 برای خرید اشتراک، /plan ارسال کنید</b>"
        await message.reply_text(text=text.format(message.from_user.mention), protect_content=True)
        await verify_user(client, userid, token)
    else:
        return await message.reply_text(text="<b>لینک نامعتبر یا لینک منقضی شده است</b>", protect_content=True)

if data.startswith("sendfiles"):
    chat_id = int("-" + file_id.split("-")[1])
    userid = message.from_user.id if message.from_user else None
    settings = await get_settings(chat_id)
    pre = 'allfilesp' if settings['file_secure'] else 'allfiles'
    g = await get_shortlink(chat_id, f"https://telegram.me/{temp.U_NAME}?start={pre}_{file_id}")
    btn = [[
        InlineKeyboardButton('دانلود اکنون', url=g)
    ]]
    if settings['tutorial']:
        btn.append([InlineKeyboardButton('چگونه دانلود کنیم', url=await get_tutorial(chat_id))])
    text = "<b>✅ فایل شما آماده است. روی دکمه دانلود اکنون کلیک کنید سپس لینک را برای دریافت فایل باز کنید\n\n</b>"
    if PREMIUM_AND_REFERAL_MODE == True:
        text += "<b>اگر می‌خواهید فایل‌های مستقیم بدون هیچ لینکی و بدون دیدن تبلیغات دریافت کنید، اشتراک ربات را بخرید ☺️\n\n💶 برای خرید اشتراک، /plan ارسال کنید</b>"
    k = await client.send_message(chat_id=message.from_user.id, text=text, reply_markup=InlineKeyboardMarkup(btn))
    await asyncio.sleep(300)
    await k.edit("<b>✅ پیام شما با موفقیت حذف شد</b>")
    return

elif data.startswith("short"):
    user = message.from_user.id
    chat_id = temp.SHORT.get(user)
    settings = await get_settings(chat_id)
    pre = 'filep' if settings['file_secure'] else 'file'
    g = await get_shortlink(chat_id, f"https://telegram.me/{temp.U_NAME}?start={pre}_{file_id}")
    btn = [[
        InlineKeyboardButton('دانلود اکنون', url=g)
    ]]
    if settings['tutorial']:
        btn.append([InlineKeyboardButton('چگونه دانلود کنیم', url=await get_tutorial(chat_id))])
    text = "<b>✅ فایل شما آماده است. روی دکمه دانلود اکنون کلیک کنید سپس لینک را برای دریافت فایل باز کنید\n\n</b>"
    if PREMIUM_AND_REFERAL_MODE == True:
        text += "<b>اگر می‌خواهید فایل‌های مستقیم بدون هیچ لینکی و بدون دیدن تبلیغات دریافت کنید، اشتراک ربات را بخرید ☺️\n\n💶 برای خرید اشتراک، /plan ارسال کنید</b>"
    k = await client.send_message(chat_id=user, text=text, reply_markup=InlineKeyboardMarkup(btn))
    await asyncio.sleep(1200)
    await k.edit("<b>✅ پیام شما با موفقیت حذف شد</b>")
    return
        
    elif data.startswith("all"):
        files = temp.GETALL.get(file_id)
        if not files:
            return await message.reply('<b><i>هیچ فایلی وجود ندارد.</b></i>')
        filesarr = []
        for file in files:
            file_id = file["file_id"]
            files1 = await get_file_details(file_id)
            title = files1["file_name"]
            size = get_size(files1["file_size"])
            f_caption = files1["caption"]
            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption = CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
                except:
                    f_caption = f_caption
            if f_caption is None:
                f_caption = f"{' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), files1['file_name'].split()))}"
            if not await db.has_premium_access(message.from_user.id):
                if not await check_verification(client, message.from_user.id) and VERIFY == True:
                    btn = [[
                        InlineKeyboardButton("تأیید", url=await get_token(client, message.from_user.id, f"https://telegram.me/{temp.U_NAME}?start="))
                    ],[
                        InlineKeyboardButton("چگونه تأیید کنم", url=VERIFY_TUTORIAL)
                    ]]
                    text = "<b>سلام {} 👋,\n\nشما امروز تأیید نشده‌اید، لطفاً روی دکمه تأیید کلیک کنید و دسترسی نامحدود برای امروز دریافت کنید</b>"
                    if PREMIUM_AND_REFERAL_MODE == True:
                        text += "<b>اگر می‌خواهید فایل‌ها را بدون تأیید دریافت کنید، اشتراک ربات را خریداری کنید ☺️\n\n💶 ارسال /plan برای خرید اشتراک</b>"
                    await message.reply_text(
                        text=text.format(message.from_user.mention),
                        protect_content=True,
                        reply_markup=InlineKeyboardMarkup(btn)
                    )
                    return
            if STREAM_MODE == True:
                button = [[InlineKeyboardButton('پخش و دانلود', callback_data=f'generate_stream_link:{file_id}')]]
                reply_markup = InlineKeyboardMarkup(button)
            else:
                reply_markup = None
            msg = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file_id,
                caption=f_caption,
                protect_content=True if pre == 'allfilesp' else False,
                reply_markup=reply_markup
            )
            filesarr.append(msg)
        k = await client.send_message(chat_id = message.from_user.id, text=f"<blockquote><b><u>❗️❗️❗️مهم❗️❗️❗️</u></b>\n\nاین پیام در <b><u>10 دقیقه</u> 🫥 <i></b> (به دلیل مسائل مربوط به حق نشر)</i> حذف خواهد شد.\n\n<b><i>لطفاً این پیام را به چت‌های ذخیره‌شده یا چت خصوصی خود ارسال کنید.</i></b></blockquote>")
        await asyncio.sleep(600)
        for x in filesarr:
            await x.delete()
        await k.edit_text("<b>✅ پیام شما با موفقیت حذف شد</b>")
        return    
        
    elif data.startswith("files"):
        user = message.from_user.id
        if temp.SHORT.get(user) == None:
            await message.reply_text(text="<b>لطفاً دوباره در گروه جستجو کنید</b>")
        else:
            chat_id = temp.SHORT.get(user)
        settings = await get_settings(chat_id)
        pre = 'filep' if settings['file_secure'] else 'file'
        if settings['is_shortlink'] and not await db.has_premium_access(user):
            g = await get_shortlink(chat_id, f"https://telegram.me/{temp.U_NAME}?start={pre}_{file_id}")
            btn = [[
                InlineKeyboardButton('دانلود هم‌اکنون', url=g)
            ]]
            if settings['tutorial']:
                btn.append([InlineKeyboardButton('چگونه دانلود کنم', url=await get_tutorial(chat_id))])
            text = "<b>✅ فایل شما آماده است، روی دکمه دانلود هم‌اکنون کلیک کنید و سپس لینک را برای دریافت فایل باز کنید\n\n</b>"
            if PREMIUM_AND_REFERAL_MODE == True:
                text += "<b>اگر می‌خواهید فایل‌ها را بدون هیچ لینک باز شونده و مشاهده تبلیغات دریافت کنید، اشتراک ربات را خریداری کنید ☺️\n\n💶 ارسال /plan برای خرید اشتراک</b>"
            k = await client.send_message(chat_id=message.from_user.id, text=text, reply_markup=InlineKeyboardMarkup(btn))
            await asyncio.sleep(1200)
            await k.edit("<b>✅ پیام شما با موفقیت حذف شد</b>")
            return
    user = message.from_user.id
    files_ = await get_file_details(file_id)           
    if not files_:
        pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
        try:
            if not await db.has_premium_access(message.from_user.id):
                if not await check_verification(client, message.from_user.id) and VERIFY == True:
                    btn = [[
                        InlineKeyboardButton("تأیید", url=await get_token(client, message.from_user.id, f"https://telegram.me/{temp.U_NAME}?start="))
                    ],[
                        InlineKeyboardButton("چگونه تأیید کنم", url=VERIFY_TUTORIAL)
                    ]]
                    text = "<b>سلام {} 👋,\n\nشما امروز تأیید نشده‌اید، لطفاً روی دکمه تأیید کلیک کنید و دسترسی نامحدود برای امروز دریافت کنید</b>"
                    if PREMIUM_AND_REFERAL_MODE == True:
                        text += "<b>اگر می‌خواهید فایل‌ها را بدون تأیید دریافت کنید، اشتراک ربات را خریداری کنید ☺️\n\n💶 ارسال /plan برای خرید اشتراک</b>"
                    await message.reply_text(
                        text=text.format(message.from_user.mention),
                        protect_content=True,
                        reply_markup=InlineKeyboardMarkup(btn)
                    )
                    return
            if STREAM_MODE == True:
    button = [[InlineKeyboardButton('پخش و دانلود', callback_data=f'generate_stream_link:{file_id}')]]
    reply_markup = InlineKeyboardMarkup(button)
else:
    reply_markup = None

msg = await client.send_cached_media(
    chat_id=message.from_user.id,
    file_id=file_id,
    protect_content=True if pre == 'filep' else False,
    reply_markup=reply_markup
)

filetype = msg.media
file = getattr(msg, filetype.value)
title = file.file_name
size = get_size(file.file_size)
f_caption = f"<code>{title}</code>"

if CUSTOM_FILE_CAPTION:
    try:
        f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title, file_size='' if size is None else size, file_caption='')
    except:
        return

await msg.edit_caption(caption=f_caption)

btn = [[InlineKeyboardButton("✅ دریافت فایل دوباره ✅", callback_data=f'del#{file_id}')]]
k = await msg.reply(text=f"<blockquote><b><u>❗️❗️❗️مهم❗️❗️❗️</u></b>\n\nاین پیام در <b><u>۱۰ دقیقه</u> 🫥 </b>حذف خواهد شد.\n\n<b><i>لطفاً این پیام را به چت خصوصی خود یا چت‌های ذخیره شده‌تان ارسال کنید.</i></b></blockquote>")

await asyncio.sleep(600)
await msg.delete()
await k.edit_text("<b>✅ پیام شما با موفقیت حذف شد. اگر می‌خواهید دوباره فایل را دریافت کنید، روی دکمه زیر کلیک کنید.</b>", reply_markup=InlineKeyboardMarkup(btn))
return
    for file_type in ("document", "video", "audio"):
    media = getattr(reply, file_type, None)
    if media is not None:
        break
else:
    await msg.edit('این فرمت فایل پشتیبانی نمی‌شود')
    return

file_id, file_ref = unpack_new_file_id(media.file_id)

result = col.delete_one({
    'file_id': file_id,
})
if not result.deleted_count:
    result = sec_col.delete_one({
        'file_id': file_id,
    })
if result.deleted_count:
    await msg.edit('فایل با موفقیت از پایگاه داده حذف شد')
else:
    file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
    unwanted_chars = ['[', ']', '(', ')']
    for char in unwanted_chars:
        file_name = file_name.replace(char, '')
    file_name = ' '.join(filter(lambda x: not x.startswith('@'), file_name.split()))

    result = col.delete_many({
        'file_name': file_name,
        'file_size': media.file_size
    })
    if not result.deleted_count:
        result = sec_col.delete_many({
            'file_name': file_name,
            'file_size': media.file_size
        })
    if result.deleted_count:
        await msg.edit('فایل با موفقیت از پایگاه داده حذف شد')
    else:
        # فایل‌های ایندکس شده قبل از این تاریخ که نام اصلی فایل را دارند
        result = col.delete_many({
            'file_name': media.file_name,
            'file_size': media.file_size
        })
        if not result.deleted_count:
            result = sec_col.delete_many({
                'file_name': media.file_name,
                'file_size': media.file_size
            })
        if result.deleted_count:
            await msg.edit('فایل با موفقیت از پایگاه داده حذف شد')
        else:
            await msg.edit('فایل در پایگاه داده پیدا نشد')


@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        'این عملیات تمام فایل‌های ایندکس شده را حذف خواهد کرد.\nآیا می‌خواهید ادامه دهید؟',
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(text="بله", callback_data="autofilter_delete")
            ],[
                InlineKeyboardButton(text="لغو", callback_data="close_data")
            ]]
        ),
        quote=True,
    )


@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, query):
    col.drop()
    sec_col.drop()
    await query.answer('دزدی اموال جرم است')
    await query.message.edit('تمام فایل‌های ایندکس شده با موفقیت حذف شدند.')
    
@Client.on_message(filters.command('settings'))
async def settings(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"شما ادمین ناشناخته هستید. برای اتصال /connect {message.chat.id} را در پیام خصوصی وارد کنید")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("مطمئن شوید که من در گروه شما هستم!!", quote=True)
                return
        else:
            await message.reply_text("من به هیچ گروهی متصل نیستم!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return
    
    settings = await get_settings(grp_id)

    try:
        if settings['max_btn']:
            settings = await get_settings(grp_id)
    except KeyError:
        await save_group_settings(grp_id, 'max_btn', False)
        settings = await get_settings(grp_id)
    if 'is_shortlink' not in settings.keys():
        await save_group_settings(grp_id, 'is_shortlink', False)
    else:
        pass

    if settings is not None:
        buttons = [
            [
                InlineKeyboardButton(
                    'صفحه نتایج',
                    callback_data=f'setgs#button#{settings["button"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'دکمه' if settings["button"] else 'متن',
                    callback_data=f'setgs#button#{settings["button"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'محافظت از محتوا',
                    callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✔ روشن' if settings["file_secure"] else '✘ خاموش',
                    callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'IMDb',
                    callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✔ روشن' if settings["imdb"] else '✘ خاموش',
                    callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'بررسی املا',
                    callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✔ روشن' if settings["spell_check"] else '✘ خاموش',
                    callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'پیام خوشامدگویی',
                    callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✔ روشن' if settings["welcome"] else '✘ خاموش',
                    callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'حذف خودکار',
                    callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '10 دقیقه' if settings["auto_delete"] else '✘ خاموش',
                    callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'فیلتر خودکار',
                    callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✔ روشن' if settings["auto_ffilter"] else '✘ خاموش',
                    callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'حداکثر دکمه‌ها',
                    callback_data=f'setgs#max_btn#{settings["max_btn"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '10' if settings["max_btn"] else f'{MAX_B_TN}',
                    callback_data=f'setgs#max_btn#{settings["max_btn"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'لینک کوتاه',
                    callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '✔ روشن' if settings["is_shortlink"] else '✘ خاموش',
                    callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{grp_id}',
                ),
            ],
        ]
        btn = [[
            InlineKeyboardButton("باز کردن اینجا ↓", callback_data=f"opnsetgrp#{grp_id}"),
            InlineKeyboardButton("باز کردن در پیام خصوصی ⇲", callback_data=f"opnsetpm#{grp_id}")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        if chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            await message.reply_text(
                text="<b>آیا می‌خواهید تنظیمات را اینجا باز کنید؟</b>",
                reply_markup=InlineKeyboardMarkup(btn),
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=message.id
            )
        else:
            await message.reply_text(
                text=f"<b>تنظیمات {title} را مطابق میل خود تغییر دهید ⚙</b>",
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=message.id
            )


@Client.on_message(filters.command('set_template'))
async def save_template(client, message):
    sts = await message.reply("در حال بررسی الگو")
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"شما مدیر ناشناس هستید. لطفاً از دستور /connect {message.chat.id} در پیام خصوصی استفاده کنید.")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("لطفاً مطمئن شوید که من در گروه شما هستم!", quote=True)
                return
        else:
            await message.reply_text("من به هیچ گروهی متصل نیستم!", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    if len(message.command) < 2:
        return await sts.edit("هیچ ورودی دریافت نشد!!")
    template = message.text.split(" ", 1)[1]
    await save_group_settings(grp_id, 'template', template)
    await sts.edit(f"با موفقیت الگو برای {title} تغییر یافت به\n\n{template}")


@Client.on_message((filters.command(["request", "Request"]) | filters.regex("#request") | filters.regex("#Request")) & filters.group)
async def requests(bot, message):
    if REQST_CHANNEL is None: return # باید کانال REQST_CHANNEL اضافه شود تا این ویژگی کار کند
    if message.reply_to_message:
        chat_id = message.chat.id
        reporter = str(message.from_user.id)
        mention = message.from_user.mention
        success = True
        content = message.reply_to_message.text
        try:
            if REQST_CHANNEL is not None:
                btn = [[
                    InlineKeyboardButton('مشاهده درخواست', url=f"{message.reply_to_message.link}"),
                    InlineKeyboardButton('نمایش گزینه‌ها', callback_data=f'show_option#{reporter}')
                ]]
                reported_post = await bot.send_message(chat_id=REQST_CHANNEL, text=f"<b>𝖱𝖾𝗉𝗈𝗋𝗍𝖾𝗋 : {mention} ({reporter})\n\n𝖬𝖾𝗌𝗌𝖺𝗀𝖾 : {content}</b>", reply_markup=InlineKeyboardMarkup(btn))
                success = True
            elif len(content) >= 3:
                for admin in ADMINS:
                    btn = [[
                        InlineKeyboardButton('مشاهده درخواست', url=f"{message.reply_to_message.link}"),
                        InlineKeyboardButton('نمایش گزینه‌ها', callback_data=f'show_option#{reporter}')
                    ]]
                    reported_post = await bot.send_message(chat_id=admin, text=f"<b>𝖱𝖾𝗉𝗈𝗋𝗍𝖾𝗋 : {mention} ({reporter})\n\n𝖬𝖾𝗌𝗌𝖺𝗀𝖾 : {content}</b>", reply_markup=InlineKeyboardMarkup(btn))
                    success = True
            else:
                if len(content) < 3:
                    await message.reply_text("<b>شما باید درخواست خود را وارد کنید [حداقل 3 کاراکتر]. درخواست‌ها نباید خالی باشند.</b>")
            if len(content) < 3:
                success = False
        except Exception as e:
            await message.reply_text(f"خطا: {e}")
            pass
        
    elif message.text:
        chat_id = message.chat.id
        reporter = str(message.from_user.id)
        mention = message.from_user.mention
        success = True
        content = message.text
        keywords = ["#request", "/request", "#Request", "/Request"]
        for keyword in keywords:
            if keyword in content:
                content = content.replace(keyword, "")
        try:
            if REQST_CHANNEL is not None and len(content) >= 3:
                btn = [[
                    InlineKeyboardButton('مشاهده درخواست', url=f"{message.link}"),
                    InlineKeyboardButton('نمایش گزینه‌ها', callback_data=f'show_option#{reporter}')
                ]]
                reported_post = await bot.send_message(chat_id=REQST_CHANNEL, text=f"<b>𝖱𝖾𝗉𝗈𝗋𝗍𝖾𝗋 : {mention} ({reporter})\n\n𝖬𝖾𝗌𝗌𝖺𝗀𝖾 : {content}</b>", reply_markup=InlineKeyboardMarkup(btn))
                success = True
            elif len(content) >= 3:
                for admin in ADMINS:
                    btn = [[
                        InlineKeyboardButton('مشاهده درخواست', url=f"{message.link}"),
                        InlineKeyboardButton('نمایش گزینه‌ها', callback_data=f'show_option#{reporter}')
                    ]]
                    reported_post = await bot.send_message(chat_id=admin, text=f"<b>𝖱𝖾𝗉𝗈𝗋𝗍𝖾𝗋 : {mention} ({reporter})\n\n𝖬𝖾𝗌𝗌𝖺𝗀𝖾 : {content}</b>", reply_markup=InlineKeyboardMarkup(btn))
                    success = True
            else:
                if len(content) < 3:
                    await message.reply_text("<b>شما باید درخواست خود را وارد کنید [حداقل 3 کاراکتر]. درخواست‌ها نباید خالی باشند.</b>")
            if len(content) < 3:
                success = False
        except Exception as e:
            await message.reply_text(f"خطا: {e}")
            pass

    else:
        success = False
    
    if success:
        link = await bot.create_chat_invite_link(int(REQST_CHANNEL))
        btn = [[
            InlineKeyboardButton('عضویت در کانال', url=link.invite_link),
            InlineKeyboardButton('مشاهده درخواست', url=f"{reported_post.link}")
        ]]
        await message.reply_text("<b>درخواست شما اضافه شد! لطفاً برای مدتی صبر کنید.\n\nابتدا به کانال بپیوندید و درخواست را مشاهده کنید</b>", reply_markup=InlineKeyboardMarkup(btn))
    
@Client.on_message(filters.command("send") & filters.user(ADMINS))
async def send_msg(bot, message):
    if message.reply_to_message:
        target_id = message.text.split(" ", 1)[1]
        out = "کاربرانی که در پایگاه داده ذخیره شده‌اند:\n\n"
        success = False
        try:
            user = await bot.get_users(target_id)
            users = await db.get_all_users()
            async for usr in users:
                out += f"{usr['id']}"
                out += '\n'
            if str(user.id) in str(out):
                await message.reply_to_message.copy(int(user.id))
                success = True
            else:
                success = False
            if success:
                await message.reply_text(f"<b>پیام شما با موفقیت به {user.mention} ارسال شد.</b>")
            else:
                await message.reply_text("<b>این کاربر هنوز ربات را شروع نکرده است!</b>")
        except Exception as e:
            await message.reply_text(f"<b>خطا: {e}</b>")
    else:
        await message.reply_text("<b>این دستور باید به عنوان پاسخ به یک پیام استفاده شود که شامل شناسه چت هدف است. مثلاً: /send userid</b>")

@Client.on_message(filters.command("deletefiles") & filters.user(ADMINS))
async def deletemultiplefiles(bot, message):
    chat_type = message.chat.type
    if chat_type != enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>سلام {message.from_user.mention}, این دستور در گروه‌ها کار نمی‌کند. فقط در پیام خصوصی کار می‌کند!</b>")
    else:
        pass
    try:
        keyword = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text(f"<b>سلام {message.from_user.mention}, لطفاً یک کلمه کلیدی همراه با دستور برای حذف فایل‌ها وارد کنید.</b>")
    k = await bot.send_message(chat_id=message.chat.id, text=f"<b>در حال جستجو برای فایل‌ها با کلمه کلیدی {keyword} در پایگاه داده... لطفاً صبر کنید...</b>")
    files, total = await get_bad_files(keyword)
    await k.delete()
    #await k.edit_text(f"<b>یافت {total} فایل برای درخواست شما {keyword} !\n\nفرآیند حذف فایل‌ها در 5 ثانیه آغاز می‌شود!</b>")
    #await asyncio.sleep(5)
    btn = [[
       InlineKeyboardButton("بله، ادامه بده!", callback_data=f"killfilesdq#{keyword}")
    ],[
       InlineKeyboardButton("نه، عملیات را لغو کن!", callback_data="close_data")
    ]]
    await message.reply_text(
        text=f"<b>یافت {total} فایل برای درخواست شما {keyword} !\n\nآیا می‌خواهید آن‌ها را حذف کنید؟</b>",
        reply_markup=InlineKeyboardMarkup(btn),
        parse_mode=enums.ParseMode.HTML
    )
@Client.on_message(filters.command("shortlink"))
async def shortlink(bot, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"شما ادمین ناشناس هستید. لطفاً ادمین ناشناس را خاموش کنید و دوباره این دستور را امتحان کنید")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>سلام {message.from_user.mention}, این دستور فقط در گروه‌ها کار می‌کند!\n\n<u>برای اتصال به کوتاه‌کننده لینک، این مراحل را دنبال کنید:</u>\n\n1. من را با حقوق کامل ادمین به گروه خود اضافه کنید\n\n2. پس از اضافه کردن به گروه، کوتاه‌کننده خود را تنظیم کنید\n\nاین دستور را در گروه خود ارسال کنید\n\n—> /shortlink \"{your_shortener_website_name} {your_shortener_api}\n\n#نمونه:-\n/shortlink kpslink.in CAACAgUAAxkBAAEJ4GtkyPgEzpIUC_DSmirN6eFWp4KInAACsQoAAoHSSFYub2D15dGHfy8E\n\nهمین! از کسب درآمد لذت ببرید 💲\n\n[[[ سایت معتبر برای کسب درآمد - https://kpslink.in]]]\n\nاگر سوالی دارید، خوشحال می‌شوم کمک کنم - @kingvj01\n\n(اگر نیاز به تماس دارید، به این شماره پیام بدهید - @kngvj01)</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    data = message.text
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return await message.reply_text("<b>شما دسترسی به استفاده از این دستور را ندارید!\n\nمن را به عنوان ادمین به گروه خود اضافه کنید و دوباره این دستور را امتحان کنید\n\nبرای اطلاعات بیشتر، با من تماس بگیرید</b>")
    else:
        pass
    try:
        command, shortlink_url, api = data.split(" ")
    except:
        return await message.reply_text("<b>دستور ناقص است :(\n\nلطفاً لینک سایت کوتاه‌کننده و API را همراه با دستور ارسال کنید!\n\nفرمت: <code>/shortlink kpslink.in e3d82cdf8f9f4783c42170b515d1c271fb1c4500</code></b>")
    reply = await message.reply_text("<b>لطفاً صبر کنید...</b>")
    shortlink_url = re.sub(r"https?://?", "", shortlink_url)
    shortlink_url = re.sub(r"[:/]", "", shortlink_url)
    await save_group_settings(grpid, 'shortlink', shortlink_url)
    await save_group_settings(grpid, 'shortlink_api', api)
    await save_group_settings(grpid, 'is_shortlink', True)
    await reply.edit_text(f"<b>API کوتاه‌کننده برای گروه {title} با موفقیت اضافه شد.\n\nسایت کوتاه‌کننده فعلی: <code>{shortlink_url}</code>\nAPI فعلی: <code>{api}</code></b>")
    
@Client.on_message(filters.command("setshortlinkoff"))
async def offshortlink(bot, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("من فقط در گروه‌ها کار می‌کنم")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return await message.reply_text("<b>شما دسترسی به استفاده از این دستور را ندارید!\n\nمن را به عنوان ادمین به گروه خود اضافه کنید و دوباره این دستور را امتحان کنید\n\nبرای اطلاعات بیشتر، با من تماس بگیرید</b>")
    else:
        pass
    await save_group_settings(grpid, 'is_shortlink', False)
    return await message.reply_text("کوتاه‌کننده با موفقیت غیرفعال شد")
    
@Client.on_message(filters.command("setshortlinkon"))
async def onshortlink(bot, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("من فقط در گروه‌ها کار می‌کنم")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return await message.reply_text("<b>شما دسترسی به استفاده از این دستور را ندارید!\n\nمن را به عنوان ادمین به گروه خود اضافه کنید و دوباره این دستور را امتحان کنید\n\nبرای اطلاعات بیشتر، با من تماس بگیرید</b>")
    else:
        pass
    settings = await get_settings(grpid)
    if not settings['shortlink']:
        return await message.reply_text("**اول باید URL و API کوتاه‌کننده خود را با دستور /shortlink تنظیم کنید، سپس می‌توانید مرا روشن کنید.**")
    await save_group_settings(grpid, 'is_shortlink', True)
    return await message.reply_text("کوتاه‌کننده با موفقیت فعال شد")

@Client.on_message(filters.command("shortlink_info"))
async def showshortlink(bot, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"شما ادمین ناشناس هستید. لطفاً ادمین ناشناس را خاموش کنید و دوباره این دستور را امتحان کنید")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>سلام {message.from_user.mention}, این دستور فقط در گروه‌ها کار می‌کند\n\nاین دستور را در گروه خود امتحان کنید، اگر از من در گروه خود استفاده می‌کنید</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    chat_id=message.chat.id
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return await message.reply_text("<b>این دستور فقط برای ادمین‌ها یا مالک گروه کار می‌کند\n\nاین دستور را در گروه خود امتحان کنید، اگر از من در گروه خود استفاده می‌کنید</b>")
    else:
        settings = await get_settings(chat_id)
        if 'shortlink' in settings.keys() and 'tutorial' in settings.keys():
            su = settings['shortlink']
            sa = settings['shortlink_api']
            st = settings['tutorial']
            return await message.reply_text(f"<b>سایت کوتاه‌کننده: <code>{su}</code>\n\nAPI: <code>{sa}</code>\n\nلینک آموزش: <code>{st}</code></b>")
        elif 'shortlink' in settings.keys() and 'tutorial' not in settings.keys():
            su = settings['shortlink']
            sa = settings['shortlink_api']
            return await message.reply_text(f"<b>سایت کوتاه‌کننده: <code>{su}</code>\n\nAPI: <code>{sa}</code>\n\nلینک آموزش متصل نشده است\n\nمی‌توانید از دستور /set_tutorial برای اتصال آن استفاده کنید</b>")
        elif 'shortlink' not in settings.keys() and 'tutorial' in settings.keys():
            st = settings['tutorial']
            return await message.reply_text(f"<b>آموزش: <code>{st}</code>\n\nURL کوتاه‌کننده متصل نشده است\n\nمی‌توانید از دستور /shortlink برای اتصال آن استفاده کنید</b>")
        else:
            return await message.reply_text("لینک کوتاه‌کننده و لینک آموزش متصل نشده‌اند. از دستورات /shortlink و /set_tutorial استفاده کنید")

@Client.on_message(filters.command("set_tutorial"))
async def settutorial(bot, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"شما ادمین ناشناس هستید. لطفاً ادمین ناشناس را خاموش کنید و دوباره این دستور را امتحان کنید")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("این دستور فقط در گروه‌ها کار می‌کند\n\nآن را در گروه خود امتحان کنید")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return
    else:
        pass
    if len(message.command) == 1:
        return await message.reply("<b>لطفاً لینک آموزش خود را همراه با این دستور ارسال کنید\n\nاستفاده از دستور: /set_tutorial لینک آموزش شما</b>")
    elif len(message.command) == 2:
        reply = await message.reply_text("<b>لطفاً صبر کنید...</b>")
        tutorial = message.command[1]
        await save_group_settings(grpid, 'tutorial', tutorial)
        await save_group_settings(grpid, 'is_tutorial', True)
        await reply.edit_text(f"<b>آموزش با موفقیت اضافه شد\n\nاین لینک آموزش برای گروه شما {title} است - <code>{tutorial}</code></b>")
    else:
        return await message.reply("<b>فرمت اشتباه وارد شده است\n\nفرمت: /set_tutorial لینک آموزش شما</b>")

@Client.on_message(filters.command("remove_tutorial"))
async def removetutorial(bot, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"شما ادمین ناشناس هستید. لطفاً ادمین ناشناس را خاموش کنید و دوباره این دستور را امتحان کنید")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("این دستور فقط در گروه‌ها کار می‌کند\n\nآن را در گروه خود امتحان کنید")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    @Client.on_message(filters.command("remove_tutorial"))
async def remove_tutorial(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"<b>شما ادمین ناشناس هستید. لطفاً ادمین ناشناس را خاموش کنید و دوباره این دستور را امتحان کنید</b>")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("<b>این دستور فقط در گروه‌ها کار می‌کند\n\nآن را در گروه خود امتحان کنید</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await client.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return
    else:
        pass
    reply = await message.reply_text("<b>لطفاً صبر کنید...</b>")
    await save_group_settings(grpid, 'tutorial', "")
    await save_group_settings(grpid, 'is_tutorial', False)
    await reply.edit_text(f"<b>لینک آموزش شما با موفقیت حذف شد!!!</b>")

@Client.on_message(filters.command("restart") & filters.user(ADMINS))
async def stop_button(bot, message):
    msg = await bot.send_message(text="**🔄 فرآیند‌ها متوقف شدند. ربات در حال راه‌اندازی مجدد است...**", chat_id=message.chat.id)       
    await asyncio.sleep(3)
    await msg.edit("**✅️ ربات با موفقیت راه‌اندازی شد. حالا می‌توانید از من استفاده کنید**")
    os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_message(filters.command("nofsub"))
async def nofsub(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"<b>شما ادمین ناشناس هستید. لطفاً ادمین ناشناس را خاموش کنید و دوباره این دستور را امتحان کنید</b>")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("<b>این دستور فقط در گروه‌ها کار می‌کند\n\nآن را در گروه خود امتحان کنید</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await client.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return
    else:
        pass
    await save_group_settings(grpid, 'fsub', None)
    await message.reply_text(f"<b>با موفقیت اشتراک اجباری از گروه {title} حذف شد.</b>")

@Client.on_message(filters.command('fsub'))
async def fsub(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"<b>شما ادمین ناشناس هستید. لطفاً ادمین ناشناس را خاموش کنید و دوباره این دستور را امتحان کنید</b>")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("<b>این دستور فقط در گروه‌ها کار می‌کند\n\nآن را در گروه خود امتحان کنید</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await client.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return
    else:
        pass
    try:
        ids = message.text.split(" ", 1)[1]
        fsub_ids = [int(id) for id in ids.split()]
    except IndexError:
        return await message.reply_text("<b>دستور ناقص است!\n\nلطفاً کانال‌ها را با فاصله وارد کنید. مثل: /fsub id1 id2 id3</b>")
    except ValueError:
        return await message.reply_text('<b>مطمئن شوید که شناسه‌ها عددی هستند.</b>')        
    channels = "کانال‌ها:\n"
    for id in fsub_ids:
        try:
            chat = await client.get_chat(id)
        except Exception as e:
            return await message.reply_text(f"<b>{id} نامعتبر است!\nمطمئن شوید که این ربات در آن کانال ادمین است.\n\nخطا - {e}</b>")
        if chat.type != enums.ChatType.CHANNEL:
            return await message.reply_text(f"<b>{id} کانال نیست.</b>")
        channels += f'{chat.title}\n'
    await save_group_settings(grpid, 'fsub', fsub_ids)
    await message.reply_text(f"<b>با موفقیت کانال‌های اجباری برای گروه {title} تنظیم شد\n\n{channels}\n\nمی‌توانید با دستور /nofsub آن را حذف کنید.</b>")
        

@Client.on_message(filters.command("add_premium"))
async def give_premium_cmd_handler(client, message):
    if PREMIUM_AND_REFERAL_MODE == False:
        return 
    user_id = message.from_user.id
    if user_id not in ADMINS:
        await message.delete()
        return
    if len(message.command) == 3:
        user_id = int(message.command[1])  # تبدیل شناسه کاربری به عدد صحیح
        time = message.command[2]        
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
            user_data = {"id": user_id, "expiry_time": expiry_time} 
            await db.update_user(user_data)  # استفاده از متد update_user برای به‌روزرسانی یا وارد کردن داده‌های کاربر
            await message.reply_text("دسترسی پریمیوم به کاربر اضافه شد.")            
            await client.send_message(
                chat_id=user_id,
                text=f"<b>پریمیوم به حساب شما برای {time} اضافه شد. از آن لذت ببرید 😀\n</b>",                
            )
        else:
            await message.reply_text("فرمت زمان نامعتبر است. لطفاً از '1day برای روزها'، '1hour برای ساعت‌ها'، یا '1min برای دقایق'، یا '1month برای ماه‌ها' یا '1year برای سال‌ها' استفاده کنید")
    else:
        await message.reply_text("<b>فرمت: /add_premium user_id time \n\nمثال: /add_premium 1252789 10day \n\n(برای واحدهای زمانی '1day برای روزها'، '1hour برای ساعت‌ها'، یا '1min برای دقایق'، یا '1month برای ماه‌ها' یا '1year برای سال‌ها')</b>")
        
@Client.on_message(filters.command("remove_premium"))
async def remove_premium_cmd_handler(client, message):
    if PREMIUM_AND_REFERAL_MODE == False:
        return
    user_id = message.from_user.id
    if user_id not in ADMINS:
        await message.delete()
        return
    if len(message.command) == 2:
        user_id = int(message.command[1])  # تبدیل شناسه کاربری به عدد صحیح
      #  time = message.command[2]
        time = "1s"
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
            user_data = {"id": user_id, "expiry_time": expiry_time}  # استفاده از "id" به جای "user_id"
            await db.update_user(user_data)  # استفاده از متد update_user برای به‌روزرسانی یا وارد کردن داده‌های کاربر
            await message.reply_text("دسترسی پریمیوم از کاربر حذف شد.")
            await client.send_message(
                chat_id=user_id,
                text="<b>پریمیوم توسط ادمین‌ها حذف شد \n\n اگر این اشتباه است، با ادمین تماس بگیرید \n\n 👮 ادمین : {} \n</b>".format(OWNER_LNK),                
            )
        else:
            await message.reply_text("فرمت زمان نامعتبر است.")
    else:
        await message.reply_text("فرمت: /remove_premium user_id")
        
@Client.on_message(filters.command("plan"))
async def plans_cmd_handler(client, message): 
    if PREMIUM_AND_REFERAL_MODE == False:
        return 
    btn = [            
        [InlineKeyboardButton("ارسال رسید پرداخت 🧾", url=OWNER_LNK)],
        [InlineKeyboardButton("⚠️ بستن / حذف ⚠️", callback_data="close_data")]
    ]
    reply_markup = InlineKeyboardMarkup(btn)
    await message.reply_photo(
        photo=PAYMENT_QR,
        caption=PAYMENT_TEXT,
        reply_markup=reply_markup
    )
        
@Client.on_message(filters.command("myplan"))
async def check_plans_cmd(client, message):
    if PREMIUM_AND_REFERAL_MODE == False:
        return 
    user_id  = message.from_user.id
    if await db.has_premium_access(user_id):         
        remaining_time = await db.check_remaining_uasge(user_id)             
        expiry_time = remaining_time + datetime.datetime.now()
        await message.reply_text(f"**جزئیات طرح شما:\n\nزمان باقی‌مانده: {remaining_time}\n\nزمان انقضا: {expiry_time}**")
    else:
        btn = [ 
            [InlineKeyboardButton("دریافت دوره آزمایشی رایگان ۵ دقیقه‌ای ☺️", callback_data="get_trail")],
            [InlineKeyboardButton("خرید اشتراک پریمیوم : حذف تبلیغات", callback_data="buy_premium")],
            [InlineKeyboardButton("⚠️ بستن / حذف ⚠️", callback_data="close_data")]
        ]
        reply_markup = InlineKeyboardMarkup(btn)
        m=await message.reply_sticker("CAACAgIAAxkBAAIBTGVjQbHuhOiboQsDm35brLGyLQ28AAJ-GgACglXYSXgCrotQHjibHgQ")         
        await message.reply_text(f"**😢 شما هیچ اشتراک پریمیومی ندارید.\n\n طرح پریمیوم ما را در /plan بررسی کنید**",reply_markup=reply_markup)
        await asyncio.sleep(2)
        await m.delete()

@Client.on_message(filters.command("totalrequests") & filters.private & filters.user(ADMINS))
async def total_requests(client, message):
    if join_db().isActive():
        total = await join_db().get_all_users_count()
        await message.reply_text(
            text=f"تعداد کل درخواست‌ها: {total}",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )

@Client.on_message(filters.command("purgerequests") & filters.private & filters.user(ADMINS))
async def purge_requests(client, message):   
    if join_db().isActive():
        await join_db().delete_all_users()
        await message.reply_text(
            text="تمام درخواست‌ها پاک شدند.",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )


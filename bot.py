# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import sys, glob, importlib, logging, logging.config, pytz, asyncio
from pathlib import Path
from datetime import date, datetime
from pyrogram import Client, idle
from aiohttp import web

# ماژول‌های داخلی پروژه
from database.users_chats_db import db
from info import *
from utils import temp
from Script import script 
from plugins import web_server
from plugins.clone import restart_bots

from TechVJ.bot import TechVJBot
from TechVJ.util.keepalive import ping_server
from TechVJ.bot.clients import initialize_clients

# تنظیمات لاگ‌گیری
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("cinemagoer").setLevel(logging.ERROR)

# بارگذاری پلاگین‌ها
ppath = "plugins/*.py"
files = glob.glob(ppath)

async def start():
    print('\n✅ ربات در حال اجرا است...')

    # بررسی وضعیت اتصال ربات
    if not await TechVJBot.is_connected:
        await TechVJBot.start()

    # گرفتن اطلاعات ربات
    bot_info = await TechVJBot.get_me()
    await initialize_clients()

    # بارگذاری پلاگین‌ها
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = "plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["plugins." + plugin_name] = load
            print(f"✅ پلاگین بارگذاری شد: {plugin_name}")

    # بررسی اجرای روی هروکو برای نگه داشتن سرور
    if ON_HEROKU:
        asyncio.create_task(ping_server())

    # دریافت کاربران و چت‌های مسدود شده
    b_users, b_chats = await db.get_banned()
    temp.BANNED_USERS = b_users
    temp.BANNED_CHATS = b_chats

    # ذخیره اطلاعات ربات در متغیرهای موقت
    me = await TechVJBot.get_me()
    temp.BOT = TechVJBot
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name

    # نمایش لوگوی ربات در لاگ‌ها
    logging.info(script.LOGO)

    # گرفتن زمان و تاریخ فعلی
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")

    # ارسال پیام ری‌استارت در کانال لاگ
    try:
        await TechVJBot.send_message(
            chat_id=LOG_CHANNEL, 
            text=script.RESTART_TXT.format(today, time)
        )
    except:
        print("⚠️ لطفاً ربات را در کانال لاگ ادمین کنید.")

    # ارسال پیام در کانال‌های فایل
    for ch in CHANNELS:
        try:
            k = await TechVJBot.send_message(chat_id=ch, text="**✅ ربات ری‌استارت شد**")
            await k.delete()
        except:
            print(f"⚠️ لطفاً ربات را در کانال {ch} با دسترسی کامل ادمین کنید.")

    # ارسال پیام در کانال فورس سابسکرایب
    try:
        k = await TechVJBot.send_message(chat_id=AUTH_CHANNEL, text="**✅ ربات ری‌استارت شد**")
        await k.delete()
    except:
        print("⚠️ لطفاً ربات را در کانال فورس سابسکرایب ادمین کنید.")

    # ری‌استارت کردن بات‌های کلون (در صورت فعال بودن و داشتن بات کلون)
    if CLONE_MODE and len(await restart_bots()) > 0:
        print("♻️ در حال ری‌استارت تمامی بات‌های کلون...")
        await restart_bots()
        print("✅ تمامی بات‌های کلون ری‌استارت شدند.")

    # راه‌اندازی وب سرور
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()

    await idle()

if name == '__main__':
    try:
        asyncio.run(start())  # ✅ استفاده از asyncio.run به جای loop.run_until_complete
    except KeyboardInterrupt:
        logging.info("🛑 سرویس متوقف شد. خداحافظ 👋")

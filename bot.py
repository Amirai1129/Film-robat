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

# بررسی مقدار TechVJBot
if TechVJBot is None:
    raise ValueError("❌ خطا: TechVJBot مقدار None دارد! لطفاً تنظیمات را بررسی کنید.")

# بارگذاری پلاگین‌ها
ppath = "plugins/*.py"
files = glob.glob(ppath)

async def start():
    print('\n✅ ربات در حال اجرا است...')
    try:
        if not TechVJBot.is_connected:
            await TechVJBot.start()
    except Exception as e:
        print(f"⚠️ خطا در استارت ربات: {e}")
        return
    
    await initialize_clients()
    
    for name in files:
        try:
            plugin_name = Path(name).stem
            import_path = f"plugins.{plugin_name}"
            spec = importlib.util.spec_from_file_location(import_path, name)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules[import_path] = load
            print(f"✅ پلاگین بارگذاری شد: {plugin_name}")
        except Exception as e:
            print(f"⚠️ خطا در بارگذاری پلاگین {plugin_name}: {e}")
    
    if ON_HEROKU:
        asyncio.create_task(ping_server())
    
    try:
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats
    except Exception as e:
        print(f"⚠️ خطا در دریافت لیست کاربران مسدود: {e}")
    
    me = await TechVJBot.get_me()
    temp.BOT = TechVJBot
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name
    
    logging.info(script.LOGO)
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")
    
    try:
        await TechVJBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))
    except:
        print("⚠️ لطفاً ربات را در کانال لاگ ادمین کنید.")
    
    for ch in CHANNELS:
        try:
            k = await TechVJBot.send_message(chat_id=ch, text="**✅ ربات ری‌استارت شد**")
            await k.delete()
        except:
            print(f"⚠️ لطفاً ربات را در کانال {ch} با دسترسی کامل ادمین کنید.")
    
    try:
        k = await TechVJBot.send_message(chat_id=AUTH_CHANNEL, text="**✅ ربات ری‌استارت شد**")
        await k.delete()
    except:
        print("⚠️ لطفاً ربات را در کانال فورس سابسکرایب ادمین کنید.")
    
    if CLONE_MODE:
        try:
            print("♻️ در حال ری‌استارت تمامی بات‌های کلون...")
            await restart_bots()
            print("✅ تمامی بات‌های کلون ری‌استارت شدند.")
        except Exception as e:
            print(f"⚠️ خطا در ری‌استارت بات‌های کلون: {e}")
    
    try:
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", PORT).start()
    except Exception as e:
        print(f"⚠️ خطا در راه‌اندازی وب سرور: {e}")
    
    await idle()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        logging.info("🛑 سرویس متوقف شد. خداحافظ 👋")
    finally:
        loop.close()

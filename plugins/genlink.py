@Client.on_message(filters.command(['link', 'plink']) & filters.create(allowed))
async def gen_link_s(bot, message):
    vj = await bot.ask(chat_id=message.from_user.id, text="Now Send Me Your Message Which You Want To Store.")
    file_type = vj.media
    if file_type not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.AUDIO, enums.MessageMediaType.DOCUMENT]:
        return await vj.reply("Send me only video, audio, file, or document.")
    if message.has_protected_content and message.chat.id not in ADMINS:
        return await message.reply("okDa")
    
    # گرفتن مقدار و چاپ برای دیباگ
    result = unpack_new_file_id((getattr(vj, file_type.value)).file_id)
    print("Unpack Output:", result)  # چاپ مقدار

    # چک کردن تعداد خروجی
    if len(result) < 2:
        return await message.reply("خطا: مقدار باز شده کمتر از حد انتظار است.")

    file_id, ref = result[:2]  # گرفتن دو مقدار اول
    string = 'filep_' if message.text.lower().strip() == "/plink" else 'file_'
    string += file_id
    outstr = base64.urlsafe_b64encode(string.encode("ascii")).decode().strip("=")
    
    await message.reply(f"Here is your Link:\nhttps://t.me/{temp.U_NAME}?start={outstr}")

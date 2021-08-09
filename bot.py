import os
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from PIL import Image
from telegraph import upload_file
from pyzbar.pyzbar import decode
import pyqrcode

TOKEN = os.environ.get("TOKEN", "")

API_ID = int(os.environ.get("API_ID", ""))

API_HASH = os.environ.get("API_HASH", "")

OWNER = os.environ.get("OWNER", "")

Deccan = Client(
        "QR CODE",
        bot_token=TOKEN,api_hash=API_HASH,
            api_id=API_ID
    )

# Commands for Bot

START_TEXT = """ 
Hello {},
 
I am simple QRcode bot.

I can generate QR code and Scan QR code.
"""
HELP_TEXT = """   
Follow these steps..
• Just send me a Text|Link, I will make a QR Code.
• Just Send me a QR Code, I will scan & Send information in it.
"""

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Owner 👨‍💻', url=f"https://telegram.me/{OWNER}")
        ],[
        InlineKeyboardButton('Tutorial 📺', url='https://telegram.me/Deccan_Supportz')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Owner 👨‍💻', url=f"https://telegram.me/{OWNER}")
        ],[
        InlineKeyboardButton('Tutorial 📺', url='https://telegram.me/Deccan_Supportz')
        ]]
    )
ERROR_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Owner 👨‍💻', url=f"https://telegram.me/{OWNER}")
        ],[
        InlineKeyboardButton('Tutorial 📺', url='https://telegram.me/Deccan_Supportz')
        ]]
    )

@Deccan.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(
       text=START_TEXT.format(update.from_user.mention),
       disable_web_page_preview=True,
       reply_markup=START_BUTTONS
    )
@Deccan.on_message(filters.private & filters.command(["help"]))
async def help(bot, update):
    await update.reply_text(
        text=HELP_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=HELP_BUTTONS
    )

# define progress for bot

async def progress(current, total, up_msg, message):
    try:
        await message.edit(
            text=f"{up_msg} {current * 100 / total:.1f}%"
        )
    except:
        pass

# qr_encode to create qr codes for text/links

@Deccan.on_message(filters.text & filters.private)
async def qr_encode(client, message):
    qr = await client.send_message(
        chat_id=message.chat.id,
        text="Making your QR Code... ✔", # Edit Text Here
        reply_to_message_id=message.message_id
    )
    s = str(message.text)
    qrname = str(message.from_user.id)
    qrcode = pyqrcode.create(s)
    qrcode.png(qrname + '.png', scale=6)
    img = qrname + '.png'
    try:
        response = upload_file(img)
    except Exception as error:
        await qr.edit_text(error)
        return
    try:
        await message.reply_photo(
            photo=img,
            progress=progress,
            progress_args=(
                "Trying to Uploading....☑", # Edit Text Here
                qr
            )
        )

    except Exception as error:
        print(error)

    
    try:
        os.remove(img)
    except Exception as error:
        print('Something is error')

# qr_decode to scan qrcodes & give message

@Deccan.on_message(filters.photo)
async def qr_decode(client, message):
    decode_text = await client.send_message(
        chat_id=message.chat.id,
        text="<b>Processing your request...✔</b>", # Edit Text Here
        reply_to_message_id=message.message_id,
    )
    dl_location = str(message.from_user.id)
    im_dowload = ''
    qr_text = ''
    try:
        im_dowload = await message.download(
            file_name=dl_location + '.png',
            progress=progress,
            progress_args=(
                "Trying to download....☑", # Edit Text Here
                decode_text
            )
        )
    except Exception as error:
        print(error)
    await decode_text.edit(
        text="Scanning..." # Edit Text Here
    )
    try:
        qr_text_data = decode(Image.open(im_dowload))
        qr_text_list = list(qr_text_data[0]) 
        qr_text_ext = str(qr_text_list[0]).split("'")[1]
        qr_text = "".join(qr_text_ext) 
    except Exception as error:
        print(error)
    await decode_text.edit_text(f"{qr_text}")
    try:
        os.remove(im_dowload)
    except Exception as error:
        print(error)

Deccan.run()

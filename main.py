import os
from pyrogram import Client
from dotenv import load_dotenv
import logging

load_dotenv()

bot_token = "6735390787:AAFgC8A7BloHiOSAJWcj8uyQJi-f_BRdlhU"
api_id = "1522127"
api_hash = "1252ffe16baf341bfd7236f92df76b0e"
plugins = dict(
    root="plugins"
)

Bot = Client(
    "URL-Shortner-Bot",
    bot_token=bot_token,
    api_id=api_id,
    api_hash=api_hash,
    plugins=plugins,
    workers=50,
    sleep_threshold=10,
)
logger.info("The bot has Started Succesfully")

Bot.run()

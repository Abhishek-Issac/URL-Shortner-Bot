import os
import aiohttp 
from .admin import *
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from pyshorteners import Shortener
import requests

BITLY_API = os.environ.get("BITLY_API", None)
CUTTLY_API = os.environ.get("CUTTLY_API", None)
SHORTCM_API = os.environ.get("SHORTCM_API", None)
GPLINKS_API = os.environ.get("GPLINKS_API", None)
POST_API = os.environ.get("POST_API", None)
OWLY_API = os.environ.get("OWLY_API", None)
ANLINKS_API = "5fe07b509a67719f0cda219f9f4cc46b1e45c0cc"

BUTTONS = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text='⚙ Support ⚙', url='https://telegram.me/goodnation')]]
)


@Client.on_message(filters.private & filters.regex(r'https?://[^\s]+'))
async def reply_shortens(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    message = await update.reply_text(
        text="`Analysing your link...`",
        disable_web_page_preview=True,
        quote=True
    )
    link = update.matches[0].group(0)
    shorten_urls = await short(update.from_user.id, link)
    await message.edit_text(
        text=shorten_urls,
        reply_markup=BUTTONS,
        disable_web_page_preview=True
    )


@Client.on_inline_query(filters.regex(r'https?://[^\s]+'))
async def inline_short(bot, update):
    link = update.matches[0].group(0)
    shorten_urls = await short(update.id, link)
    answers = [
        InlineQueryResultArticle(
            title="Short Link From Anlinks.in",
            description=update.query,
            input_message_content=InputTextMessageContent(
                message_text=shorten_urls,
                disable_web_page_preview=True
            ),
            reply_markup=BUTTONS
        )
    ]
    await bot.answer_inline_query(
        inline_query_id=update.id,
        results=answers
    )

async def short(chat_id, link):
    shorten_urls = "**--Shortened URLs--**\n"

    # Assuming ANLINKS_API is defined somewhere in your code
    if ANLINKS_API and await db.allow_domain(chat_id, "anlinks.in"):
        try:
            # Replace 'your_api_url_here' with the actual API URL
            api_url = 'your_api_url_here'
            response = requests.get(api_url)
            response_data = response.json()

            if response_data["status"] == "success":
                shortened_url = response_data["shortenedUrl"]
                shorten_urls += f"\n**Anlinks.in :-** {shortened_url}"
            else:
                print(f"Anlinks API error: {response_data.get('error', 'Unknown error')}")

        except Exception as error:
            print(f"Anlinks API request error: {error}")

    shorten_urls += "\n\nMade by @Goodnation"
    
    return shorten_urls

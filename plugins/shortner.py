import os
import aiohttp 
from .admin import *
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from pyshorteners import Shortener


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
    
    if ANLINKS_API and await db.allow_domain(chat_id, "anlinks.in"):
        try:
            api_url = "https://anlinks.in/api"
            params = {'api': ANLINKS_API, 'url': link}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, params=params, raise_for_status=True) as response:
                    data = await response.json()
                    shortened_url = data.get("shortenedUrl")
                    
                    if shortened_url:
                        shorten_urls += f"\n**Anlinks.in :-** {shortened_url}"
                    else:
                        shorten_urls += "\nFailed to shorten the URL using Anlinks.in"
        except aiohttp.ClientError as error:
            print(f"AnLinks error: {error}")
    
    shorten_urls += "\n\nMade by @Goodnation"
    
    return shorten_urls

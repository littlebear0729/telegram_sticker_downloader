import json
import logging
from webptools import dwebp

from tgs2gif import tgs2gif
from webm2gif import webm2gif
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "This bot is used for download all kinds of stickers.\nNow under construction, be patience.")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def static_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    r = await update.message.reply_text('Static sticker detected, downloading...')
    file = await update.message.effective_attachment.get_file()
    print(file)
    await file.download_to_drive(f'files/{file.file_id}.webp')

    await r.edit_text('Sticker downloaded, converting...')
    dwebp(f'files/{file.file_id}.webp', f'files/{file.file_id}.png', option='-o', logging='-v')

    await r.edit_text('Convert completed, sending file...')
    await update.message.reply_document(f'files/{file.file_id}.png', filename=f'{file.file_id[-8:]}.png.1')

    await r.delete()


async def animated_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    r = await update.message.reply_text('Animated sticker detected, downloading...')
    file = await update.message.effective_attachment.get_file()
    print(file)
    await file.download_to_drive(f'files/{file.file_id}.tgs')

    await r.edit_text('Sticker downloaded, converting...')
    tgs2gif(f'files/{file.file_id}.tgs')

    await r.edit_text('Convert completed, sending file...')
    await update.message.reply_document(f'files/{file.file_id}.gif', filename=f'{file.file_id[-8:]}.gif.1')

    await r.delete()


async def video_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    r = await update.message.reply_text('Video sticker detected, downloading...')
    file = await update.message.effective_attachment.get_file()
    print(file)
    await file.download_to_drive(f'files/{file.file_id}.webm')

    await r.edit_text('Sticker downloaded, converting...')
    webm2gif(f'files/{file.file_id}.webm')

    await r.edit_text('Convert completed, sending file...')
    await update.message.reply_document(f'files/{file.file_id}.gif', filename=f'{file.file_id[-8:]}.gif.1')

    await r.delete()


def main(bot_token: str) -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(bot_token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # handle stickers
    application.add_handler(MessageHandler(filters.Sticker.STATIC, static_sticker))
    application.add_handler(MessageHandler(filters.Sticker.ANIMATED, animated_sticker))
    application.add_handler(MessageHandler(filters.Sticker.VIDEO, video_sticker))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


def read_config():
    f = open('config.json', 'r')
    conf = json.loads(f.read())
    f.close()
    return conf


if __name__ == "__main__":
    config = read_config()
    token = config['token']
    main(token)

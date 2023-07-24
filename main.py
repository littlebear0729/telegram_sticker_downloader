import json
import logging
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
    file = await update.message.effective_attachment.get_file()
    print(file)
    await file.download_to_drive(f'files/{file.file_id}.webp')
    pass


async def animated_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file = await update.message.effective_attachment.get_file()
    print(file)
    await file.download_to_drive(f'files/{file.file_id}.tgs')
    pass


async def video_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file = await update.message.effective_attachment.get_file()
    print(file)
    await file.download_to_drive(f'files/{file.file_id}.webm')
    pass


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

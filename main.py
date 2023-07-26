import json
import logging
from webptools import dwebp

# from tgs2gif import tgs2gif
# from webm2gif import webm2gif
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


async def add_whitelist(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update.message.text)
    user_id = update.message.text.split(' ')[-1]
    try:
        config['whitelist'].append(int(user_id))
        with open('config.json', 'w') as f:
            f.write(json.dumps(config))
    except Exception as e:
        print(e)
        await update.message.reply_text(str(e))
    else:
        await update.message.reply_text(f'Add {user_id} to whitelist, current whitelist: {whitelist}')


async def list_whitelist(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Current admin:{admin}\n\nCurrent whitelist:{whitelist}')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)
    user_id = update.message.chat_id
    print(user_id, user_id in admin, user_id in whitelist)


def has_permission(chat_id: int) -> bool:
    if chat_id in admin or chat_id in whitelist:
        return True
    else:
        return False


async def static_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not has_permission(update.message.chat_id):
        return
    r = await update.message.reply_text('Static sticker detected, downloading...')
    file = await update.message.effective_attachment.get_file()
    print(file)
    await file.download_to_drive(f'files/{file.file_unique_id}.webp')

    await r.edit_text('Sticker downloaded, converting...')
    dwebp(f'files/{file.file_unique_id}.webp', f'files/{file.file_unique_id}.png', option='-o', logging='-v')

    await r.edit_text('Convert completed, sending file...')
    await update.message.reply_document(f'files/{file.file_unique_id}.png', filename=f'{file.file_unique_id}.png.1')

    await r.delete()


async def animated_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not has_permission(update.message.chat_id):
        return
    r = await update.message.reply_text('Animated sticker detected, downloading...')
    file = await update.message.effective_attachment.get_file()
    print(file)
    await file.download_to_drive(f'files/{file.file_unique_id}.tgs')

    await r.edit_text('Sticker downloaded, converting...')
    # tgs2gif(f'files/{file.file_unique_id}.tgs')

    await r.edit_text('Convert completed, sending file...')
    await update.message.reply_document(f'files/{file.file_unique_id}.gif', filename=f'{file.file_unique_id}.gif.1')

    await r.delete()


async def video_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not has_permission(update.message.chat_id):
        return
    r = await update.message.reply_text('Video sticker detected, downloading...')
    file = await update.message.effective_attachment.get_file()
    print(file)
    await file.download_to_drive(f'files/{file.file_unique_id}.webm')

    await r.edit_text('Sticker downloaded, converting...')
    # webm2gif(f'files/{file.file_unique_id}.webm')

    await r.edit_text('Convert completed, sending file...')
    await update.message.reply_document(f'files/{file.file_unique_id}.gif', filename=f'{file.file_unique_id}.gif.1')

    await r.delete()


async def sticker_set(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sticker_set_name = update.message.text.split('/')[-1]
    print(sticker_set_name)
    set = await context.bot.get_sticker_set(sticker_set_name)
    print(set.is_animated, set.is_video, set.title)
    for sticker in set.stickers:
        print(sticker)


def main(bot_token: str) -> None:
    print(admin, whitelist)
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(bot_token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("add_whitelist", add_whitelist, filters=filters.User(admin)))
    application.add_handler(CommandHandler("list_whitelist", list_whitelist, filters=filters.User(admin)))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.Regex(r'^https://t.me/addstickers/'), sticker_set))
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


admin = []
whitelist = []

if __name__ == "__main__":
    config = read_config()
    token = config['token']
    admin = config['admin']
    whitelist = config['whitelist']
    main(token)

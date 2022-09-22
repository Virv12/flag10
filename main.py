import logging
import re

from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext

from flag import craft_flag
from sub import get_sub

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def flag_handler(update: Update, context: CallbackContext):
    if m := re.match(r'^/flag\[(\d+)\]$', update.message.text):
        n = int(m.group(1))
        flag = craft_flag(n)
    else:
        flag = craft_flag()

    update.message.reply_text(flag, parse_mode=ParseMode.MARKDOWN)

def sub_handler(update: Update, context: CallbackContext):
    update.message.reply_text(get_sub(), parse_mode=ParseMode.MARKDOWN)

def main():
    token = open('.token').read().strip()

    # Create the Updater and pass it your bot's token.
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('flag', flag_handler))
    dispatcher.add_handler(CommandHandler('sub', sub_handler))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()

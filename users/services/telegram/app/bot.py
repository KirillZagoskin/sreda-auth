from email import message
from django.conf import settings
from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from telegram.utils.request import Request

from users.services.authentication import register


def answer_to_user(update: Update, context: CallbackContext):
    msg, reply_markup = register.platform_access(update, context)
    update.message.reply_text(text=msg, reply_markup=reply_markup)


request = Request(
    connect_timeout=0.5,
    read_timeout=1.0,
)
bot = Bot(request=request, token=settings.TELEGRAM_API_TOKEN)

updater = Updater(
    bot=bot,
    use_context=True
)

message_handler = MessageHandler(Filters.text, answer_to_user)
updater.dispatcher.add_handler(message_handler)
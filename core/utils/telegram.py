import logging

from config import settings
from telegram.bot import Bot

from core.utils.singleton import SingletonDecorator

logger = logging.getLogger(__name__)

SingletonTelegramBot = SingletonDecorator(Bot)
MY_CHAT_ID = 772974581
bot = SingletonTelegramBot(settings.TELEGRAM_TOKEN)


def send_message(chat_id, text):
    return bot.send_message(chat_id, text)


def send_me(text):
    return bot.send_message(MY_CHAT_ID, text)

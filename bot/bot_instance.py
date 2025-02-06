import logging.config
from aiogram import Bot
from api.config.logging import LOGGING
from bot.config.bot import TELEGRAM_API_TOKEN
from aiogram.client.default import DefaultBotProperties

# LOGGING
logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

bot = Bot(TELEGRAM_API_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from dotenv import load_dotenv

from app.api_request import RequestAPI

load_dotenv()


bot = Bot(token=os.getenv('BOT_TOKEN'),
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
requester = RequestAPI()

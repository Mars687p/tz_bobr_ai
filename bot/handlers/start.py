from aiogram import Router, types
from aiogram.filters import Command

from app.logs import logger
from bot.services.keyboards import create_kb_receipt_weather

router = Router()


@logger.catch
@router.message(Command(commands=['start', 'help']))
async def send_help(message: types.Message) -> types.Message:
    kb = create_kb_receipt_weather()
    text = ('Здравствуйте!\n'
            'Хотите узнать погоду? \n'
            )
    return await message.answer(text=text, reply_markup=kb)

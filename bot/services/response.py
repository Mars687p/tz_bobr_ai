from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardMarkup


async def is_long_message(text: str) -> str | list[str]:
    if len(text) > 4090:
        lst_sms = []
        for x in range(0, len(text), 4090):
            lst_sms.append(text[x:x+4090])
        return lst_sms
    return text


async def send_response(message: types.Message,
                        text: str,
                        kb: InlineKeyboardMarkup | None = None) -> None:
    format_text = await is_long_message(text)
    if type(format_text) is list:
        for sms in format_text:
            await message.answer(sms, reply_markup=kb)
    if type(format_text) is str:
        await message.answer(format_text, reply_markup=kb)

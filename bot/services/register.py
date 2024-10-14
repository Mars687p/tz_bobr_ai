from aiogram import types

from app.config import bot


async def register_commands() -> None:
    await bot.set_my_commands([
                                types.BotCommand(command="help",
                                                 description="Помощь")
                              ]
                              )

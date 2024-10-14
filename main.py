import asyncio

from app.config import bot, dp, requester
from bot.handlers import get_weather, start
from bot.services.register import register_commands


async def start_app() -> None:
    try:
        await requester.get_session()
        await register_commands()
        dp.include_routers(start.router, get_weather.router)
        await dp.start_polling(bot)
    finally:
        await requester.close_session()

if __name__ == '__main__':
    asyncio.run(start_app())

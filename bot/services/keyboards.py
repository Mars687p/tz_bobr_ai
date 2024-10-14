from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from bot.services.callback_factory import GetWeather


def create_kb_receipt_weather() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Погода сейчас',
        callback_data=GetWeather(
                        action="get_weather_city_now",).pack()
    )
    builder.button(
        text='Прогноз погоды',
        callback_data=GetWeather(
                        action="get_weather_city_forecast",).pack()
    )
    builder.adjust(1)
    return builder.as_markup()

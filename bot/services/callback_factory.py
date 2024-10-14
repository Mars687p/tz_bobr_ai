from typing import Literal

from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import State, StatesGroup


class WeatherState(StatesGroup):
    enter_city_now = State()
    enter_city_forecast = State()


class GetWeather(CallbackData, prefix="weather"):  # type: ignore
    action: Literal['get_weather_city_forecast',
                    'get_weather_city_now',]

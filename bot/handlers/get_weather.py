from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.config import requester
from app.exceptions import (EmptyResponseGeocoder, RequestGeocoderUncomplited,
                            RequestWeatherUncomplited)
from bot.services.callback_factory import GetWeather, WeatherState
from bot.services.keyboards import create_kb_receipt_weather
from bot.services.response import send_response

router = Router()


@router.callback_query(StateFilter(None),
                       GetWeather.filter(
                           F.action.in_(("get_weather_city_now",
                                        'get_weather_city_forecast'))))
async def get_weather_by_city(callback: types.CallbackQuery,
                              state: FSMContext) -> None:
    action = ''
    if callback.data:
        action = callback.data.split('weather:')[1]
    await callback.message.answer(text="Напишите город")  # type: ignore
    if action == 'get_weather_city_now':
        await state.set_state(WeatherState.enter_city_now)
    elif action == 'get_weather_city_forecast':
        await state.set_state(WeatherState.enter_city_forecast)


@router.message(WeatherState.enter_city_now)
async def enter_city_now(message: types.Message,
                         state: FSMContext) -> None:
    await state.clear()
    try:
        city = await requester.get_coord_by_name(f'"{message.text}"')
    except EmptyResponseGeocoder:
        await message.answer('Город не найден')
        return
    except RequestGeocoderUncomplited:
        await message.answer('Не удалось выполнить запрос. Повторите попытку позже')
        return

    try:
        weather = await requester.get_weather_now(city)
    except RequestWeatherUncomplited:
        await message.answer('Не удалось выполнить запрос. Повторите попытку позже')
        return

    kb = create_kb_receipt_weather()
    await message.answer(text=(
            f"{city['country']} {city['state']} {city['name']}\n"
            f"<b>Описание:</b> {weather['data']['weather_description']}\n"
            f"<b>Температура:</b> {weather['data']['temp']}\n"
            f"<b>Ощущается как:</b> {weather['data']['temp_feels_like']}\n"
            f"<b>Скорость ветра:</b> {weather['data']['wind_speed']}\n"
            f"<b>Давление:</b> {weather['data']['pressure']}\n"
            f"<b>Влажность:</b> {weather['data']['humidity']}\n"
            f"<b>Над уровнем моря:</b> {weather['data']['sea_lvl']}\n"
            f"<b>Восход солнца:</b> {weather['sunrise'].time()}\n"
            f"<b>Заход солнца:</b> {weather['sunset'].time()}\n"
            ), reply_markup=kb
    )


@router.message(WeatherState.enter_city_forecast)
async def enter_city_forecast(
                        message: types.Message,
                        state: FSMContext) -> None:
    await state.clear()
    try:
        city = await requester.get_coord_by_name(f'"{message.text}"')
    except EmptyResponseGeocoder:
        await message.answer('Город не найден')
        return
    except RequestGeocoderUncomplited:
        await message.answer('Не удалось выполнить запрос. Повторите попытку позже')
        return

    try:
        weather = await requester.get_weather_forecast(city)
    except RequestWeatherUncomplited:
        await message.answer('Не удалось выполнить запрос. Повторите попытку позже')
        return

    text = (
            f"{city['country']} {city['state']} {city['name']}\n"
            f"<b>Восход солнца:</b> {weather['sunrise'].time()}\n"
            f"<b>Заход солнца:</b> {weather['sunset'].time()}\n\n"
            )

    kb = create_kb_receipt_weather()
    # Прогноз погоды на сутки. 8 * 3 = 24
    for forecast in weather['list_forecast'][:9]:
        text += (
                f"<b>{forecast['dt_txt']}</b>\n"
                f"<b>Описание:</b> {forecast['weather_description']}\n"
                f"<b>Температура:</b> {forecast['temp']}\n"
                f"<b>Ощущается как:</b> {forecast['temp_feels_like']}\n"
                f"<b>Скорость ветра:</b> {forecast['wind_speed']}\n"
                f"<b>Давление:</b> {forecast['pressure']}\n"
                f"<b>Влажность:</b> {forecast['humidity']}\n"
                f"<b>Над уровнем моря:</b> {forecast['sea_lvl']}\n\n\n"
                )

    await send_response(message, text, kb)

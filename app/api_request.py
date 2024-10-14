import asyncio
import os
from datetime import datetime
from typing import Any, Dict

import aiohttp

from .exceptions import (EmptyResponseGeocoder, RequestGeocoderUncomplited,
                         RequestUncomplited, RequestWeatherUncomplited)
from .logs import logger
from .types import (CityResponseDict, WeatherDataDict, WeatherDataWithForecast,
                    WeatherForecastDict, WeatherNowDict)

HEADERS = {'user-agent':
           ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/129.0.0.0 Safari/537.36'
            )}

SERVICE_WEATHER_KEY = os.getenv('SERVICE_WEATHER_KEY')

URL_API_GEOCODER = os.getenv('URL_API_GEOCODER').format(
                                key=SERVICE_WEATHER_KEY, city='{city}')
URL_API_WEATHER_NOW = os.getenv('URL_API_WEATHER_NOW').format(
                                key=SERVICE_WEATHER_KEY,
                                lat='{lat}', lon='{lon}')
URL_API_WEATHER_FORECAST = os.getenv('URL_API_WEATHER_FORECAST').format(
                                key=SERVICE_WEATHER_KEY,
                                lat='{lat}', lon='{lon}')


class RequestAPI:
    def __init__(self) -> None:
        self.session: aiohttp.ClientSession

    async def get_session(self) -> None:
        self.session = aiohttp.ClientSession(headers=HEADERS)

    async def _execute_request(self, url: str) -> list[Dict[str, Any]]:
        try:
            async with self.session.get(url) as resp:
                return await resp.json()
        except (OSError,
                aiohttp.client_exceptions.ServerDisconnectedError,
                asyncio.TimeoutError) as err:
            logger.exception(err)
            raise RequestUncomplited('Запрос не выполнен')

    async def get_coord_by_name(self,
                                city_name: str,) -> CityResponseDict:
        url = URL_API_GEOCODER.format(city=city_name)
        try:
            response = await self._execute_request(url)
        except RequestUncomplited:
            raise RequestGeocoderUncomplited('Запрос геокодера не выполнен')

        if not response:
            raise EmptyResponseGeocoder()
        return CityResponseDict({
            'name': city_name,
            'country': response[0].get('country'),
            'state': response[0].get('state'),
            'longitude': response[0].get('lon'),
            'latitude': response[0].get('lat'),
        })

    async def get_weather_now(
                        self,
                        city: CityResponseDict) -> WeatherNowDict:
        url = URL_API_WEATHER_NOW.format(
                                        lat=city['latitude'],
                                        lon=city['longitude'])
        try:
            response = await self._execute_request(url)
        except RequestUncomplited:
            raise RequestWeatherUncomplited
        return WeatherNowDict(
                    sunrise=datetime.fromtimestamp(response['sys']['sunrise']),
                    sunset=datetime.fromtimestamp(response['sys']['sunset']),
                    data=WeatherDataDict(
                        weather_description=response['weather'][0]['description'],
                        temp=response['main']['temp'],
                        temp_feels_like=response['main']['feels_like'],
                        pressure=response['main']['pressure'],
                        humidity=response['main']['humidity'],
                        sea_lvl=response['main']['sea_level'],
                        wind_speed=response['wind']['speed'],
                        ),
                    )

    async def get_weather_forecast(
                        self,
                        city: CityResponseDict) -> WeatherForecastDict:
        url = URL_API_WEATHER_FORECAST.format(
                                        lat=city['latitude'],
                                        lon=city['longitude'])
        try:
            response = await self._execute_request(url)
        except RequestWeatherUncomplited:
            raise RequestWeatherUncomplited

        list_forecast = WeatherForecastDict(
                    sunrise=datetime.fromtimestamp(response['city']['sunrise']),
                    sunset=datetime.fromtimestamp(response['city']['sunset']),
                    list_forecast=[])
        for weather in response['list']:
            list_forecast['list_forecast'].append(
                    WeatherDataWithForecast(
                        weather_description=weather['weather'][0]['description'],
                        temp=weather['main']['temp'],
                        temp_feels_like=weather['main']['feels_like'],
                        pressure=weather['main']['pressure'],
                        humidity=weather['main']['humidity'],
                        sea_lvl=weather['main']['sea_level'],
                        wind_speed=weather['wind']['speed'],
                        dt_txt=weather['dt_txt']
                    ),
                )
        return list_forecast

    async def close_session(self) -> None:
        await self.session.close()

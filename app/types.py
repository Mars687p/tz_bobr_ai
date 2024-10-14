from datetime import datetime
from decimal import Decimal
from typing import TypedDict


class CityResponseDict(TypedDict):
    name: str
    country: str
    state: str | None
    longitude: Decimal
    latitude: Decimal


class WeatherDataDict(TypedDict):
    weather_description: str
    temp: float
    temp_feels_like: float
    pressure: int
    humidity: int
    sea_lvl: int
    wind_speed: float


class WeatherDataWithForecast(WeatherDataDict):
    dt_txt: str


class WeatherNowDict(TypedDict):
    sunrise: datetime
    sunset: datetime
    data: WeatherDataDict


class WeatherForecastDict(TypedDict):
    sunrise: datetime
    sunset: datetime
    list_forecast: list[WeatherDataWithForecast]

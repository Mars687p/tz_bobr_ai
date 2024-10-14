class RequestUncomplited(Exception):
    "Запрос не выполнен"


class RequestGeocoderUncomplited(Exception):
    "Запрос получения координат города не выполнен"


class RequestWeatherUncomplited(Exception):
    "Запрос получения погоды не выполнен"


class EmptyResponseGeocoder(Exception):
    """Не удалось найти город"""

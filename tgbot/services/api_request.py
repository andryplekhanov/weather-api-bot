import requests
from requests.models import Response
from typing import Dict, Union


def request_to_api(url: str, querystring: Dict, headers: Union[Dict, None] = None) -> Union[Response, None]:
    """
    Функция осуществляет get-запрос к api. Если ответ == 200: возвращает результат, иначе None.
    :param url: строка с энд-пойнтом для запроса.
    :param querystring: словарь с параметрами для запроса.
    :param headers: словарь с "X-Yandex-API-Key"
    :return: ответ от api или None
    """
    try:
        request = requests.get(url=url, params=querystring, headers=headers)
        if request.status_code == requests.codes.ok:
            return request
    except Exception:
        return None

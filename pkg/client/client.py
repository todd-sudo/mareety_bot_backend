from typing import List, Union, Optional

import requests
from django.conf import settings

from config.logger.logger import logger as log
from pkg.client.exeptions import HTTP_EXCEPTIONS


class HttpClient:
    """ HTTP Клиент
    """
    url: str
    headers: dict
    cookies: dict
    json_data: Union[dict, list]
    data: any

    def __init__(
            self,
            url: str,
            headers: Optional[dict] = None,
            cookies: Optional[dict] = None,
            json_data: Union[dict, list, None] = None,
            data: any = None
    ):
        if cookies is None:
            cookies = {}
        if headers is None:
            headers = {}

        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.data = data
        self.json_data = json_data

    def _get(self,):
        response = requests.get(
            url=self.url,
            headers=self.headers,
            cookies=self.cookies,
        )
        return response

    def _post_json(self):
        response = requests.post(
            url=self.url,
            headers=self.headers,
            cookies=self.cookies,
            json=self.json_data
        )
        return response

    def _post_data(self):
        response = requests.post(
            url=self.url,
            headers=self.headers,
            cookies=self.cookies,
            data=self.data
        )
        return response

    def http_get(self) -> Optional[requests.Response]:
        """ Отправляет GET запрос
        """
        for i in range(settings.HTTP_CLIENT_COUNT_REQUEST_RETRY + 1):
            try:
                response = self._get()
                if response and response.status_code == 200:
                    return response
            except HTTP_EXCEPTIONS as err:
                log.error(
                    f"{i} [http_get] Ошибка отправки GET запраса - {err}"
                )
                continue
            continue

    def http_post_json(self) -> Optional[requests.Response]:
        """ Отправляет POST запрос с JSON
        """
        for i in range(settings.HTTP_CLIENT_COUNT_REQUEST_RETRY + 1):
            try:
                response = self._post_json()
                if response and response.status_code == 200:
                    return response
            except HTTP_EXCEPTIONS as err:
                log.error(
                    f"{i} [http_post_json] Ошибка отправки POST запраса - {err}"
                )
                continue
            continue

    def http_post_data(self) -> Optional[requests.Response]:
        """ Отправляет POST запрос с другими данными
        """
        for i in range(settings.HTTP_CLIENT_COUNT_REQUEST_RETRY + 1):
            try:
                response = self._post_data()
                if response and response.status_code == 200:
                    return response
            except HTTP_EXCEPTIONS as err:
                log.error(
                    f"{i} [http_post_data] Ошибка отправки POST запраса - {err}"
                )
                continue
            continue

    @staticmethod
    def decode_json(
            response: requests.Response
    ) -> Union[List[dict], dict, List[list], None]:
        """ Декодирование JSON из ответа
        """
        try:
            data = response.json()
            return data
        except HTTP_EXCEPTIONS as err:
            log.error(
                f"[http_get_json] Ошибка декодирования JSON - {err}"
            )
            return None

    @staticmethod
    def http_get_text(response: requests.Response) -> Optional[str]:
        """ Получает текст ответа в виде строки
        """
        response_text = response.text
        return response_text

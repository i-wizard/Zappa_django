import requests

from decouple import config
from .error_handler import RequestMethodError


class OneApiConfig():
    one_api_secret: str = config("ONEAPI_SECRET")
    base_url: str = 'https://the-one-api.dev/v2/'
    headers: dict = {"Authorization": f"Bearer {one_api_secret}"}

    def parse_url(self, path: str) -> str:
        return f'{self.base_url}{path}'

    def parse_response(self, response) -> dict:
        data = response.json()
        return {"status": response.status_code, "data": data}

    def handle_request(self, method, url, data=None) -> dict:
        request_map = {
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "DELETE": requests.delete
        }
        request = request_map.get(method)
        if not request:
            raise RequestMethodError('This method is currently not available')
        response = request(url, headers=self.headers, json=data)
        if f'{response.status_code}'.startswith('2'):
            final_response = self.parse_response(response)
            response_status = True
        else:
            final_response = response.json()
            response_status = False
        return {"status": response.status_code, "data": {**final_response, "status": response_status}}

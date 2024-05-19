import requests as r


class HousefireAPI:
    def __init__(self, api_key: str):
        self.base_url = "https://housefire.liammurphydev.com/api/"
        self.api_key = api_key
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
        }

    def __construct_url(self, endpoint: str):
        if endpoint.startswith("/") and len(endpoint) > 1:
            return self.base_url + endpoint[1:]
        return self.base_url + endpoint

    def __get(self, endpoint, params=None) -> r.Response:
        return r.get(
            self.__construct_url(endpoint), headers=self.headers, params=params
        )

    def __post(self, endpoint, data=None) -> r.Response:
        return r.post(self.__construct_url(endpoint), headers=self.headers, json=data)

    def __delete(self, endpoint) -> r.Response:
        return r.delete(self.__construct_url(endpoint), headers=self.headers)

    def get_properties_by_ticker(self, ticker: str) -> r.Response:
        return self.__get(f"/properties/{ticker}")

    def delete_properties_by_ticker(self, ticker: str) -> r.Response:
        return self.__delete(f"/properties/{ticker}")

    def post_properties(self, data) -> r.Response:
        return self.__post(f"/properties", data)

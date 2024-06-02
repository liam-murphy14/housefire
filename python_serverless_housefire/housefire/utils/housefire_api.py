import requests as r
from housefire.utils.logger import get_logger

logger = get_logger(__name__)


class HousefireAPI:
    """
    Housefire API client

    Args:
        api_key (str): Housefire API key
    """

    def __init__(self, api_key: str):
        self.base_url = "https://housefire.liammurphydev.com/api/"
        self.api_key = api_key
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
        }
        logger.debug("Housefire API client initialized")

    def __construct_url(self, endpoint: str):
        full_url = self.base_url + endpoint
        if endpoint.startswith("/") and len(endpoint) > 1:
            full_url = self.base_url + endpoint[1:]
        logger.debug(f"Constructed URL: {full_url}")
        return full_url

    def __get(self, endpoint, params=None) -> r.Response:
        logger.debug(f"GET request to {endpoint} with params: {params}")
        response = r.get(
            self.__construct_url(endpoint), headers=self.headers, params=params
        )
        logger.debug(f"GET request to {endpoint} returned: {response}")
        return response

    def __post(self, endpoint, data=None) -> r.Response:
        logger.debug(f"POST request to {endpoint} with data: {data}")
        response = r.post(
            self.__construct_url(endpoint), headers=self.headers, json=data
        )
        logger.debug(f"POST request to {endpoint} returned: {response}")
        return response

    def __delete(self, endpoint) -> r.Response:
        logger.debug(f"DELETE request to {endpoint}")
        response = r.delete(self.__construct_url(endpoint), headers=self.headers)
        logger.debug(f"DELETE request to {endpoint} returned: {response}")
        return response

    def get_properties_by_ticker(self, ticker: str) -> r.Response:
        return self.__get(f"/properties/{ticker}")

    def delete_properties_by_ticker(self, ticker: str) -> r.Response:
        return self.__delete(f"/properties/{ticker}")

    def post_properties(self, data) -> r.Response:
        return self.__post(f"/properties", data)

import requests as r
import time
from housefire.logger import get_logger
import googlemaps

logger = get_logger(__name__)


class HousefireAPI:
    """
    Housefire API client

    Args:
        api_key (str): Housefire API key
    """

    def __init__(
        self, api_key: str, base_url: str = "https://housefire.liammurphydev.com/api/"
    ):
        self.base_url = base_url
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
        logger.debug(f"with data: {response.json()}")
        return response

    def __delete(self, endpoint) -> r.Response:
        logger.debug(f"DELETE request to {endpoint}")
        response = r.delete(self.__construct_url(endpoint), headers=self.headers)
        logger.debug(f"DELETE request to {endpoint} returned: {response}")
        return response

    def get_properties_by_ticker(self, ticker: str) -> r.Response:
        return self.__get(f"/properties/byTicker/{ticker}")

    def delete_properties_by_ticker(self, ticker: str) -> r.Response:
        return self.__delete(f"/properties/byTicker/{ticker}")

    def post_properties(self, data) -> r.Response:
        return self.__post(f"/properties", data)

    def get_geocode_by_address_input(self, address_input: str) -> r.Response:
        return self.__get(f"/geocode/byAddressInput/{address_input}")

    def post_geocode(self, data) -> r.Response:
        return self.__post(f"/geocode", data)


class GoogleGeocodeAPI:

    def __init__(self, api_key: str, housefire_api_client: HousefireAPI):
        self.api_key = api_key
        self.client = googlemaps.Client(key=api_key)
        self.housefire_api_client = housefire_api_client
        self.wait_time = 72  # wait 72 seconds between geocoding requests to limit to 1200 requests per day

    def geocode_addresses(self, address_inputs: list[str]) -> dict[str, dict]:
        """
        geocodes a list of addresses and returns a dictionary of address inputs to housefire geocode results
        """
        results = dict()
        for address_input in address_inputs:
            logger.debug(
                f"checking if address input {address_input} is already in housefire"
            )
            housefire_res = self.housefire_api_client.get_geocode_by_address_input(address_input)
            logger.debug(f"housefire response: {housefire_res}")
            if housefire_res.status_code == 200:
                logger.debug(f"address input {address_input} already in housefire")
                results[address_input] = (
                    housefire_res.json().data
                )  # ??? TODO: check this
                time.sleep(1) # hacky rate limit
                continue
            logger.debug(f"geocoding address input {address_input}")
            google_geocode_response = self.client.geocode(address_input)
            logger.debug(
                f"geocoded address input {address_input} with response: {google_geocode_response}"
            )
            if len(google_geocode_response.results) == 0:
                logger.error(f"no results found for address input {address_input}")
                continue

            housefire_geocode = self.__google_geocode_to_housefire_geocode(
                google_geocode_response.results[0]
            )
            logger.debug(
                f"converted google geocode to housefire geocode: {housefire_geocode}"
            )
            housefire_geocode["addressInput"] = address_input
            housefire_geocode_response_data = self.housefire_api_client.post_geocode(
                housefire_geocode
            ).json()
            logger.debug(
                f"posted housefire geocode: {housefire_geocode} with response: {housefire_geocode_response_data}"
            )
            results[address_input] = (
                housefire_geocode_response_data.data
            )  # ??? TODO: check this
            time.sleep(self.wait_time)
        return results

    def __google_geocode_to_housefire_geocode(self, google_geocode: dict) -> dict:
        (
            street_number,
            route,
            locality,
            administrative_area_level_1,
            administrative_area_level_2,
            country,
            postal_code,
        ) = (None, None, None, None, None, None, None)
        for component in google_geocode["address_components"]:
            for component_type in component["types"]:
                if component_type == "street_number":
                    street_number = component["long_name"]
                elif component_type == "route":
                    route = component["long_name"]
                elif component_type == "locality":
                    locality = component["long_name"]
                elif component_type == "administrative_area_level_1":
                    administrative_area_level_1 = component["long_name"]
                elif component_type == "administrative_area_level_2":
                    administrative_area_level_2 = component["long_name"]
                elif component_type == "country":
                    country = component["long_name"]
                elif component_type == "postal_code":
                    postal_code = component["long_name"]

        return {
            "streetNumber": street_number,
            "route": route,
            "locality": locality,
            "administrativeAreaLevel1": administrative_area_level_1,
            "administrativeAreaLevel2": administrative_area_level_2,
            "country": country,
            "postalCode": postal_code,
            "formattedAddress": google_geocode["formatted_address"],
            "globalPlusCode": google_geocode["plus_code"]["global_code"],
            "latitude": google_geocode["geometry"]["location"]["lat"],
            "longitude": google_geocode["geometry"]["location"]["lng"],
        }

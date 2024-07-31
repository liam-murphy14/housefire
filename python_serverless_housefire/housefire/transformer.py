import pandas as pd
import numpy as np
from housefire.housefire_api import HousefireAPI
from housefire.logger import get_logger
import dotenv
from housefire.utils import get_env_nonnull, parse_and_convert_area, df_to_request

logger = get_logger(__name__)

PLD_UNNECESSARY_COLUMNS = [
    "Available Date",
    "Market Property Type",
    "Link To Property Search Page",
    "Digital Tour URL",
    "Video URL",
    "Microsite URL",
    "Property Marketing Collateral URL",
    "Truck Court Depth",
    "Rail Served",
    "Broker Name",
    "Broker Email Address",
    "Broker Telephone Number",
    "Leasing Agent Name",
    "Leasing Agent Email Address",
    "Leasing Agent Telephone Number",
    "Unit Name",
    "Unit Office Size",
    "# of Grade Level Doors",
    "Warehouse Lighting Type",
    "Clear Height",
    "Main Breaker Size (AMPS)",
    "Fire Suppression System",
    "# of Dock High Doors",
    "Key Feature 1",
    "Key Feature 2",
    "Key Feature 3",
    "Key Feature 4",
    "Key Feature 5",
    "Key Feature 6",
]

PLD_COLUMN_NAMES_MAP = {
    "Property Name": "name",
    "Street Address 1": "address",
    "Street Address 2": "address2",
    "Neighborhood": "neighborhood",
    "City": "city",
    "State": "state",
    "Postal Code": "zip",
    "Country": "country",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Available Square Footage": "squareFootage",
}


def _pld_transform(df: pd.DataFrame) -> pd.DataFrame:
    df.drop(
        columns=PLD_UNNECESSARY_COLUMNS,
        inplace=True,
        axis=1,
    )
    df.rename(
        PLD_COLUMN_NAMES_MAP,
        inplace=True,
        axis=1,
    )
    df = df.astype({"zip": "str"})
    df['squareFootage'] = df['squareFootage'].apply(parse_and_convert_area)
    return df


TRANSFORMERS = {
    "pld": _pld_transform,
}


def transform_wrapper(data: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """
    Transform data and log
    """
    custom_transform = TRANSFORMERS[ticker]
    logger.debug(f"Transforming data for REIT: {ticker}, df: {data}")
    transformed_data = custom_transform(data)
    transformed_data.fillna(np.nan, inplace=True)
    transformed_data.replace([np.nan], [None], inplace=True)
    transformed_data_with_ticker = transformed_data.assign(reitTicker=ticker.upper())
    logger.debug(f"Transformed data for REIT: {ticker}, df: {transformed_data_with_ticker}")
    return transformed_data_with_ticker


if __name__ == '__main__':
    dotenv.load_dotenv()

    HOUSEFIRE_API_KEY = get_env_nonnull("HOUSEFIRE_API_KEY")

    api = HousefireAPI(HOUSEFIRE_API_KEY)
    api.base_url = "http://localhost:5173/api/"
    pld_test_df = pd.read_csv("/Users/liammurphy/Downloads/Data_export.csv")
    transformed = transform_wrapper(pld_test_df, "pld")
    request = df_to_request(transformed)
    response = api.post_properties(request)
    logger.info(f"resjsno: {response.json()}")

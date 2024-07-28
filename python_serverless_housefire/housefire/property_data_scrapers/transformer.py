import pandas as pd
from housefire.utils.logger import get_logger

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
    "Street Address 1": "address_1",
    "Street Address 2": "address_2",
    "Neighborhood": "neighborhood",
    "City": "city",
    "State": "state",
    "Postal Code": "zip_code",
    "Country": "country",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Available Square Footage": "square_footage",
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
    df.fillna("", inplace=True)
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
    logger.debug(f"Transformed data for REIT: {ticker}, df: {transformed_data}")
    return transformed_data


def df_to_request(df: pd.DataFrame, ticker: str):
    """
    Convert a pandas DataFrame to a list of dictionaries
    """
    logger.debug(
        f"Converting DataFrame to request format with REIT: {ticker} for df: {df}"
    )
    df_with_reit = df.assign(reit=ticker)
    request_dict = df_with_reit.to_dict(orient="records")
    logger.debug(f"Converted DataFrame to request format: {request_dict}")
    return request_dict

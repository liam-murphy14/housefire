import pandas as pd
from housefire.utils.logger import get_logger

logger = get_logger(__name__)


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


class Transformer:
    """
    Base class for data transformers
    """

    def __init__(self, ticker: str):
        self.logger = get_logger(self.__class__.__name__)
        self.ticker = ticker

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Transform data and log
        """
        self.logger.debug(f"Transforming data for REIT: {self.ticker}, df: {data}")
        transformed_data = self.custom_transform(data)
        self.logger.debug(
            f"Transformed data for REIT: {self.ticker}, df: {transformed_data}"
        )
        return transformed_data

    def custom_transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Transform data
        """
        raise NotImplementedError

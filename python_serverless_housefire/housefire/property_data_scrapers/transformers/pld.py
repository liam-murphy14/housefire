import pandas as pd
from housefire.property_data_scrapers.transformers.common import Transformer


class PldTransformer(Transformer):
    """
    Transformer for PLD data
    """

    def __init__(self):
        super().__init__("PLD")
        self.UNNECESSARY_COLUMNS = [
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

        self.COLUMN_NAMES_MAP = {
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

    def custom_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df.drop(
            columns=self.UNNECESSARY_COLUMNS,
            inplace=True,
            axis=1,
        )
        df.rename(
            self.COLUMN_NAMES_MAP,
            inplace=True,
            axis=1,
        )
        df.fillna("", inplace=True)
        return df

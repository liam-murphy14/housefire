import pandas as pd
import redis
from dotenv import load_dotenv
import os
from urllib.parse import urlparse
import uuid

UNNECESSARY_COLUMNS = [
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
COLUMN_NAMES_MAP = {
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


def parse_pld_properties():
    df = pd.read_csv(REIT_CSV_LOCATION)
    df.drop(
        axis=1,
        columns=UNNECESSARY_COLUMNS,
        inplace=True,
    )
    df.rename(
        COLUMN_NAMES_MAP,
        inplace=True,
        axis=1,
    )
    df = df.assign(id=[str(uuid.uuid4()) for _ in range(len(df))])
    df.fillna("", inplace=True)
    property_list = df.to_dict(orient="records")
    redis_url = os.getenv("KV_URL")
    if not redis_url:
        raise Exception("Missing KV_URL in environment")

    url_obj = urlparse(redis_url)
    host = url_obj.hostname
    port = url_obj.port
    username = url_obj.username
    password = url_obj.password
    ssl = True
    if not host or not port:
        raise Exception("Missing host or port in KV_URL")

    r = redis.Redis(
        host=host,
        port=port,
        username=username,
        password=password,
        ssl=ssl,
    )

    r.json().set("properties:PLD", "$", property_list)

    os.remove(REIT_CSV_LOCATION)


if __name__ == "__main__":
    load_dotenv()

    TEMP_DIR = os.getenv("TEMP_DIR")
    if TEMP_DIR is None:
        raise Exception("Missing TEMP_DIR in environment")
    REIT_CSV_LOCATION = os.path.join(TEMP_DIR, "pld_properties.csv")
    parse_pld_properties()

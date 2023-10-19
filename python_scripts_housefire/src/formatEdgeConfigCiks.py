import requests as r
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

TEMP_DIR_PATH = os.getenv("TEMP_DIR")
if TEMP_DIR_PATH is None:
    raise Exception("TEMP_DIR environment variable not set")
REIT_CSV_PATH = os.path.join(TEMP_DIR_PATH, "reits.csv")

CIK_ENDPOINT = "https://sec.gov/files/company_tickers.json"


def format_edge_config_ciks():
    to_concat_list = ["{"]
    reit_csv = pd.read_csv(REIT_CSV_PATH)
    reit_set = set(reit_csv["Symbol"])
    cik_res = r.get(CIK_ENDPOINT)
    cik_data = cik_res.json()
    for key in cik_data:
        cik_str, ticker = str(cik_data[key]["cik_str"]), cik_data[key]["ticker"]
        if ticker not in reit_set:
            continue
        cik_str = cik_str.zfill(10)
        to_concat_list.append(f'     "{ticker}": "{cik_str}",')
    to_concat_list.append("}")
    return "\n".join(to_concat_list)


if __name__ == "__main__":
    if not os.path.exists(REIT_CSV_PATH):
        raise Exception(f"{REIT_CSV_PATH} does not exist")
    formatted_ciks = format_edge_config_ciks()
    print(formatted_ciks)

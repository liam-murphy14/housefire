from housefire.logger import get_logger
import pandas as pd
import time
import os
import nodriver as uc

logger = get_logger(__name__)


async def _pld_scrape(tab: uc.Tab, temp_dir_path: str) -> pd.DataFrame:
    # find and click the hidden button to download the csv
    download_button = await tab.select("#download_results")
    if download_button is None:
        raise Exception("could not find download button")
    if not isinstance(download_button, uc.Element):
        raise Exception("could not find download button")
    await download_button.click()

    csv_download_button = await tab.select("#download_results_csv")
    if csv_download_button is None:
        raise Exception("could not find download button")
    if not isinstance(csv_download_button, uc.Element):
        raise Exception("could not find download button")
    await csv_download_button.click()
    time.sleep(10)

    file_list = list(filter(lambda filename : not filename.startswith("."), os.listdir(temp_dir_path)))

    if len(file_list) == 0:
        raise Exception("could not find downloaded csv")

    logger.debug(
        f"downloaded pld csv, temp_dir_path: {temp_dir_path}, files: {file_list}"
    )

    # get the downloaded file, hacky but works
    filepath = os.path.join(temp_dir_path, file_list[0])
    logger.debug(f"reading csv file: {filepath}")
    df = pd.read_csv(filepath)
    logger.debug("deleting csv")
    os.remove(filepath)
    return df


SCRAPERS = {
    "pld": _pld_scrape,
}

START_URLS = {
    "pld": "https://www.prologis.com/property-search?at=building%3Bland%3Bland_lease%3Bland_sale%3Bspec_building&bounding_box%5Btop_left%5D%5B0%5D=-143.31501&bounding_box%5Btop_left%5D%5B1%5D=77.44197&bounding_box%5Bbottom_right%5D%5B0%5D=163.24749&bounding_box%5Bbottom_right%5D%5B1%5D=-60.98419&ms=uscustomary&lsr%5Bmin%5D=0&lsr%5Bmax%5D=9007199254740991&bsr%5Bmin%5D=0&bsr%5Bmax%5D=9007199254740991&so=metric_size_sort%2Cdesc&p=0&m=&an=0",
}


async def scrape_wrapper(
    driver: uc.Browser, ticker: str, temp_dir_path: str
) -> pd.DataFrame:
    """
    Scrape data and log
    """
    start_url = START_URLS[ticker]
    custom_scraper = SCRAPERS[ticker]

    logger.debug(f"Scraping data for REIT: {ticker}")
    logger.debug(f"navigating to {start_url}")
    tab = await driver.get(start_url)
    logger.debug(f"Navigated to {start_url}")
    scraped_data = await custom_scraper(tab, temp_dir_path)
    logger.debug(f"Scraped data for REIT: {ticker}, df: {scraped_data}")
    return scraped_data


import sys
import dotenv
import housefire.undetected_chromedriver.options
import housefire.utils.scraping_utils
import housefire.property_data_scrapers.scrapers.pld
from housefire.property_data_scrapers.transformers.common import df_to_request
import housefire.property_data_scrapers.transformers.pld
import undetected_chromedriver as uc
from housefire.utils.env_utils import (
    get_env_nonnull_dir,
    get_env_nonnull_file,
    get_env_nonnull,
)
from housefire.utils.housefire_api import HousefireAPI
from housefire.utils.logger import get_logger

logger = get_logger(__name__)

SCRAPERS = {
    "pld": housefire.property_data_scrapers.scrapers.pld.Scraper,
}

TRANSFORMERS = {
    "pld": housefire.property_data_scrapers.transformers.pld.Transformer,
}


def get_chromedriver_instance(random_temp_dir_path: str) -> uc.Chrome:
    """
    Get a new instance of the undetected_chromedriver Chrome driver
    """
    CHROMEDRIVER_PATH = get_env_nonnull_file("CHROMEDRIVER_PATH")
    CHROME_PATH = get_env_nonnull_file("CHROME_PATH")
    # enable downloading files from selenium
    options = housefire.undetected_chromedriver.options.Options()
    preferences = {
        "download.default_directory": random_temp_dir_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
    }
    options.add_experimental_option("prefs", preferences)

    return uc.Chrome(
        options=options,
        headless=True,
        driver_executable_path=CHROMEDRIVER_PATH,
        browser_executable_path=CHROME_PATH,
    )


def main():

    dotenv.load_dotenv()

    TEMP_DIR_PATH = get_env_nonnull_dir("TEMP_DIR_PATH")

    HOUSEFIRE_API_KEY = get_env_nonnull("HOUSEFIRE_API_KEY")

    random_temp_dir_path = housefire.utils.scraping_utils.create_temp_dir(TEMP_DIR_PATH)

    try:
        driver = get_chromedriver_instance(random_temp_dir_path)
    except Exception as e:
        logger.critical(f"Failed to create chromedriver instance: {e}")
        housefire.utils.scraping_utils.delete_temp_dir(random_temp_dir_path)
        raise e

    try:
        if len(sys.argv) != 2:
            raise Exception("Usage: python main.py <ticker>")

        ticker = sys.argv[1].lower()
        logger.info(f"Scraping data for ticker: {ticker}")

        if ticker not in SCRAPERS or ticker not in TRANSFORMERS:
            raise ValueError(f"Unsupported ticker: {ticker}")

        scraper = SCRAPERS[ticker](ticker, driver, random_temp_dir_path)
        logger.debug(f"Using scraper: {scraper}")
        transformer = TRANSFORMERS[ticker](ticker)
        logger.debug(f"Using transformer: {transformer}")

        properties_dataframe = scraper.scrape()
        logger.debug(f"Scraped properties data: {properties_dataframe}")
        transformed_dataframe = transformer.transform(properties_dataframe)
        logger.debug(f"Transformed properties data: {transformed_dataframe}")

        housefire_api = HousefireAPI(HOUSEFIRE_API_KEY)

        housefire_api.delete_properties_by_ticker(ticker.upper())
        housefire_api.post_properties(
            df_to_request(transformed_dataframe, ticker.upper())
        )

    finally:
        driver.quit()
        housefire.utils.scraping_utils.delete_temp_dir(random_temp_dir_path)


if __name__ == "__main__":
    main()

import sys
import dotenv
from housefire.scraper import (
    SCRAPERS,
    START_URLS,
    scrape_wrapper,
)
from housefire.transformer import (
    TRANSFORMERS,
    df_to_request,
    transform_wrapper,
)
import nodriver as uc
from housefire.utils import (
    get_env_nonnull_dir,
    get_env_nonnull_file,
    get_env_nonnull,
)
from housefire.housefire_api import HousefireAPI
from housefire.logger import get_logger

logger = get_logger(__name__)


async def get_chromedriver_instance() -> uc.Browser:
    """
    Get a new instance of the undetected_chromedriver Chrome driver
    """
    CHROME_PATH = get_env_nonnull_file("CHROME_PATH")

    return await uc.start(
        headless=True,
        browser_executable_path=CHROME_PATH,
    )


async def main():

    dotenv.load_dotenv()

    TEMP_DIR_PATH = get_env_nonnull_dir("TEMP_DIR_PATH")

    HOUSEFIRE_API_KEY = get_env_nonnull("HOUSEFIRE_API_KEY")

    try:
        driver = await get_chromedriver_instance()
    except Exception as e:
        logger.critical(f"Failed to create chromedriver instance: {e}")
        raise e

    try:
        if len(sys.argv) != 2:
            raise Exception("Usage: python main.py <ticker>")

        ticker = sys.argv[1].lower()
        logger.info(f"Scraping data for ticker: {ticker}")

        if (
            ticker not in SCRAPERS
            or ticker not in START_URLS
            or ticker not in TRANSFORMERS
        ):
            raise ValueError(f"Unsupported ticker: {ticker}")

        properties_dataframe = await scrape_wrapper(driver, ticker, TEMP_DIR_PATH)
        logger.debug(f"Scraped properties data: {properties_dataframe}")
        transformed_dataframe = transform_wrapper(properties_dataframe, ticker)
        logger.debug(f"Transformed properties data: {transformed_dataframe}")

        housefire_api = HousefireAPI(HOUSEFIRE_API_KEY)

        housefire_api.delete_properties_by_ticker(ticker.upper())
        housefire_api.post_properties(
            df_to_request(transformed_dataframe)
        )

    finally:
        driver.stop()


if __name__ == "__main__":
    uc.loop().run_until_complete(main())

from housefire.utils.logger import get_logger
import pandas as pd
import undetected_chromedriver as uc


class Scraper:
    """
    Base class for data scrapers
    """

    def __init__(
        self, ticker: str, driver: uc.Chrome, temp_dir_path: str, start_url: str = ""
    ):
        self.logger = get_logger(self.__class__.__name__)
        self.ticker = ticker
        self.driver = driver
        self.temp_dir_path = temp_dir_path
        self.start_url = start_url

    def scrape(self) -> pd.DataFrame:
        """
        Scrape data and log
        """
        self.logger.debug(f"Scraping data for REIT: {self.ticker}")
        self.logger.debug(f"navigating to {self.start_url}")
        self.driver.get(self.start_url)
        self.logger.debug(f"Navigated to {self.start_url}")
        scraped_data = self.custom_scrape()
        self.logger.debug(f"Scraped data for REIT: {self.ticker}, df: {scraped_data}")
        return scraped_data

    def custom_scrape(self) -> pd.DataFrame:
        """
        Transform data
        """
        raise NotImplementedError

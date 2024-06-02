import undetected_chromedriver as uc
import pandas as pd
import os
from selenium.webdriver.common.by import By
import time
from housefire.property_data_scrapers.scrapers.common import Scraper

PLD_URL = "https://www.prologis.com/property-search?at=building%3Bland%3Bland_lease%3Bland_sale%3Bspec_building&bounding_box%5Btop_left%5D%5B0%5D=-143.31501&bounding_box%5Btop_left%5D%5B1%5D=77.44197&bounding_box%5Bbottom_right%5D%5B0%5D=163.24749&bounding_box%5Bbottom_right%5D%5B1%5D=-60.98419&ms=uscustomary&lsr%5Bmin%5D=0&lsr%5Bmax%5D=9007199254740991&bsr%5Bmin%5D=0&bsr%5Bmax%5D=9007199254740991&so=metric_size_sort%2Cdesc&p=0&m=&an=0"


class PldScraper(Scraper):
    """
    Scraper for Prologis property data
    """

    def __init__(self, ticker: str, driver: uc.Chrome, temp_dir_path: str):
        super().__init__("PLD", driver, temp_dir_path, PLD_URL)

    def scrape(self) -> pd.DataFrame:
        # find and click the hidden button to download the csv
        self.driver.find_element(By.ID, "download_results").click()
        self.driver.find_element(By.ID, "download_results_csv").click()
        time.sleep(10)

        # get the downloaded file, hacky but works
        filepath = os.path.join(self.temp_dir_path, os.listdir(self.temp_dir_path)[0])
        return pd.read_csv(filepath)

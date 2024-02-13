import undetected_chromedriver as uc
from dotenv import load_dotenv
import os
from selenium.webdriver.common.by import By
from lib.undetected_chromedriver.options import Options
import time


PLD_URL = "https://www.prologis.com/property-search?at=building%3Bland%3Bland_lease%3Bland_sale%3Bspec_building&bounding_box%5Btop_left%5D%5B0%5D=-143.31501&bounding_box%5Btop_left%5D%5B1%5D=77.44197&bounding_box%5Bbottom_right%5D%5B0%5D=163.24749&bounding_box%5Bbottom_right%5D%5B1%5D=-60.98419&ms=uscustomary&lsr%5Bmin%5D=0&lsr%5Bmax%5D=9007199254740991&bsr%5Bmin%5D=0&bsr%5Bmax%5D=9007199254740991&so=metric_size_sort%2Cdesc&p=0&m=&an=0"


def download_pld_properties(temp_dir_path: str, chrome_path: str, chromedriver_path: str):
    options = Options()
    preferences = {
        "download.default_directory": os.path.join(temp_dir_path, "pld_props"),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
    }
    options.add_experimental_option("prefs", preferences)

    driver = uc.Chrome(
        options=options,
        headless=IS_HEADLESS,
        driver_executable_path=chromedriver_path,
        browser_executable_path=chrome_path,
    )
    driver.get(PLD_URL)

    # find and click the hidden button to download the csv
    driver.find_element(By.ID, "download_results").click()
    driver.find_element(By.ID, "download_results_csv").click()
    time.sleep(10)
    driver.quit()


def move_pld_properties(temp_dir: str):
    # move the csv to the temp directory
    downloaded_file = os.listdir(os.path.join(temp_dir, "pld_props"))[0]
    os.rename(
        os.path.join(temp_dir, "pld_props", downloaded_file),
        REIT_CSV_LOCATION,
    )
    os.removedirs(os.path.join(temp_dir, "pld_props"))


if __name__ == "__main__":
    load_dotenv()

    TEMP_DIR = os.getenv("TEMP_DIR")
    CHROME_PATH = os.getenv("CHROME_PATH")
    CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")
    if TEMP_DIR is None:
        raise Exception("Missing TEMP_DIR in environment")
    if CHROME_PATH is None:
        raise Exception("Missing CHROME_PATH in environment")
    if CHROMEDRIVER_PATH is None:
        raise Exception("Missing CHROMEDRIVER_PATH in environment")
    REIT_CSV_LOCATION = os.path.join(TEMP_DIR, "pld_properties.csv")

    IS_HEADLESS = False if os.getenv("DEPLOY_ENV") == "development" else True

    download_pld_properties(TEMP_DIR, CHROME_PATH, CHROMEDRIVER_PATH)
    move_pld_properties(TEMP_DIR)

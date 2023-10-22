import undetected_chromedriver as uc
from dotenv import load_dotenv
import os
from selenium.webdriver.common.by import By
from lib.undetected_chromedriver.options import Options

load_dotenv()

TEMP_DIR = os.getenv("TEMP_DIR")
if TEMP_DIR is None:
    raise Exception("Missing TEMP_DIR in environment")
REIT_CSV_LOCATION = os.path.join(TEMP_DIR, "pld_properties.csv")
DRIVER_PATH = os.path.join(TEMP_DIR, "chromedriver")
CHROME_PATH = os.getenv("CHROME_PATH")

IS_HEADLESS = False if os.getenv("DEPLOY_ENV") == "development" else True


def download_pld_properties():
    driver = uc.Chrome(
        options=Options(),
        headless=IS_HEADLESS,
        driver_executable_path=DRIVER_PATH,
        browser_executable_path=CHROME_PATH,
    )
    driver.get("https://google.com")
    els = driver.find_elements(By.CSS_SELECTOR, "a")
    print(els)


if __name__ == "__main__":
    download_pld_properties()

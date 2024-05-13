import sys
import os
import dotenv
import housefire.undetected_chromedriver.options
import housefire.utils.scraping_utils
import housefire.property_data_scrapers.scrapers.pld
import housefire.property_data_scrapers.transformers.pld
import undetected_chromedriver as uc

SCRAPERS = {
    "pld": housefire.property_data_scrapers.scrapers.pld.scrape,
}

TRANSFORMERS = {
    "pld": housefire.property_data_scrapers.transformers.pld.transform,
}


def main():

    dotenv.load_dotenv()

    TEMP_DIR_PATH = os.getenv("TEMP_DIR")
    if TEMP_DIR_PATH is None:
        raise Exception("TEMP_DIR environment variable not set")
    if not os.path.exists(TEMP_DIR_PATH):
        raise Exception(f"{TEMP_DIR_PATH} does not exist")
    if not os.path.isdir(TEMP_DIR_PATH):
        raise Exception(f"{TEMP_DIR_PATH} is not a directory")

    CHROME_PATH = os.getenv("CHROME_PATH")
    if CHROME_PATH is None:
        raise Exception("CHROME_PATH environment variable not set")
    if not os.path.exists(CHROME_PATH):
        raise Exception(f"{CHROME_PATH} does not exist")
    if not os.path.isfile(CHROME_PATH):
        raise Exception(f"{CHROME_PATH} is not a file")

    CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")
    if CHROMEDRIVER_PATH is None:
        raise Exception("CHROMEDRIVER_PATH environment variable not set")
    if not os.path.exists(CHROMEDRIVER_PATH):
        raise Exception(f"{CHROMEDRIVER_PATH} does not exist")
    if not os.path.isfile(CHROMEDRIVER_PATH):
        raise Exception(f"{CHROMEDRIVER_PATH} is not a file")

    random_temp_dir = housefire.utils.scraping_utils.create_temp_dir(TEMP_DIR_PATH)

    # enable downloading files from selenium
    options = housefire.undetected_chromedriver.options.Options()
    preferences = {
        "download.default_directory": os.path.join(random_temp_dir, "pld_props"),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
    }
    options.add_experimental_option("prefs", preferences)

    driver = uc.Chrome(
        options=options,
        headless=True,
        driver_executable_path=CHROMEDRIVER_PATH,
        browser_executable_path=CHROME_PATH,
    )

    ticker = sys.argv[1]

    if ticker not in SCRAPERS or ticker not in TRANSFORMERS:
        raise Exception(f"Unsupported ticker: {ticker}")

    scrape = SCRAPERS[ticker]
    transform = TRANSFORMERS[ticker]

    properties_dataframe = scrape(driver, random_temp_dir)
    transformed_dataframe = transform(properties_dataframe)

    # TODO: do diff and save to DB

    housefire.utils.scraping_utils.delete_temp_dir(random_temp_dir)

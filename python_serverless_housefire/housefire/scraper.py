from housefire.logger import get_logger
import pandas as pd
import time
import os
import nodriver as uc
import random as r

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

    file_list = list(
        filter(lambda filename: not filename.startswith("."), os.listdir(temp_dir_path))
    )

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


async def _eqix_scrape(tab: uc.Tab, temp_dir_path: str) -> pd.DataFrame:
    df_list = list()
    city_urls = await _eqix_scrape_city_urls(tab)
    logger.debug(f"found city urls: {city_urls}")
    property_urls = list()
    for city_url in city_urls:
        jiggle_time = r.randint(10, 70)
        time.sleep(jiggle_time)
        city_tab = await tab.browser.get(city_url, new_tab=True)
        property_urls.extend(await _eqix_scrape_single_city_property_urls(city_tab))
        await city_tab.close()
    logger.debug(f"found property urls: {property_urls}")

    for property_url in property_urls:
        jiggle_time = r.randint(10, 70)
        time.sleep(jiggle_time)
        property_tab = await tab.browser.get(property_url, new_tab=True)
        df = await _eqix_scrape_single_property(property_tab)
        await property_tab.close()
        # TODO: add caching here so that a bad scrape does not lose all data
        df_list.append(df)

    return pd.concat(df_list)


async def _eqix_scrape_city_urls(tab: uc.Tab) -> list[str]:
    tab_content = await tab.select(".tabs-content")
    link_elements = await tab_content.query_selector_all(".regions_metro-link")
    logger.debug(f"found link elements: {link_elements}")
    return [link_element.attrs["href"] for link_element in link_elements]


async def _eqix_scrape_single_city_property_urls(tab: uc.Tab) -> list[str]:
    urls_to_scrape = list()
    try:
        dropdown_menu_button = await tab.select("#dropdownMenuButton")
        logger.debug(f"dropdown_menu_button: {dropdown_menu_button}")
        dropdown_menu_list = (await tab.select(".ibx-dropdown")).children[0].children
        logger.debug(f"found dropdown_menu_list: {dropdown_menu_list}")
        urls_to_scrape = [item.attrs["href"] for item in dropdown_menu_list]
    except TimeoutError as e:
        logger.debug("no dropdown menu button, looking for primary button")
        primary_button_list = await tab.select_all(".btn-primary")
        logger.debug(f"primary_button_list: {primary_button_list}")
        primary_buttons_with_real_href = list(
            filter(
                lambda button: "href" in button.attrs and button.attrs["href"] != "#",
                primary_button_list,
            )
        )
        primary_button = (
            primary_buttons_with_real_href[0]
            if len(primary_buttons_with_real_href) > 0
            else None
        )
        logger.debug(f"primary_button: {primary_button}")
        if primary_button is None:
            raise Exception("could not find primary button")
        urls_to_scrape.append(primary_button.attrs["href"])

    return urls_to_scrape


async def _eqix_scrape_single_property(tab: uc.Tab) -> pd.DataFrame:
    name_div = await tab.select(".hero-slice-sub-headline")
    short_name_div = await tab.select(".hero-slice-headline")
    logger.debug(f"name divs: {name_div}\n\n {short_name_div}")
    name = f"{short_name_div.text.strip()} - {name_div.text.strip()}"
    logger.debug(f"scraping property with name: {name}")

    contact_div = await tab.select(".ibx-contact")
    logger.debug(f"contact div: {contact_div}")

    address_div = contact_div.children[0].children[0].children[0]
    logger.debug(f"address_div: {address_div}")

    # some properties only have address line 2
    address_line_1_div, address_line_2_div = None, None
    if len(address_div.children) > 2:
        address_line_1_div = address_div.children[1]
        logger.debug(f"address_line_1_div: {address_line_1_div}")
        address_line_2_div = address_div.children[2]
        logger.debug(f"address_line_2_div: {address_line_2_div}")
    elif len(address_div.children) == 2:
        logger.debug("address_div has 2 children, assuming only address line 2")
        address_line_2_div = address_div.children[1]
        logger.debug(f"address_line_2_div: {address_line_2_div}")
    else:
        raise Exception("could not find address div children")

    address_part_list = address_line_2_div.text.strip().split(",")
    logger.debug(f"address parts: {address_part_list}")
    zip_code = address_part_list[-1].strip()
    country = address_part_list[-2].strip()
    city = address_part_list[0].strip()
    state = None
    if len(address_part_list) >= 4:
        state = address_part_list[1].strip()

    address = (
        address_line_1_div.text.strip() if address_line_1_div is not None else None
    )

    return pd.DataFrame(
        {
            "name": [name],
            "address": [address],
            "city": [city],
            "state": [state],
            "zip": [zip_code],
            "country": [country],
        }
    )


SCRAPERS = {
    "pld": _pld_scrape,
    "eqix": _eqix_scrape,
}

START_URLS = {
    "pld": "https://www.prologis.com/property-search?at=building%3Bland%3Bland_lease%3Bland_sale%3Bspec_building&bounding_box%5Btop_left%5D%5B0%5D=-143.31501&bounding_box%5Btop_left%5D%5B1%5D=77.44197&bounding_box%5Bbottom_right%5D%5B0%5D=163.24749&bounding_box%5Bbottom_right%5D%5B1%5D=-60.98419&ms=uscustomary&lsr%5Bmin%5D=0&lsr%5Bmax%5D=9007199254740991&bsr%5Bmin%5D=0&bsr%5Bmax%5D=9007199254740991&so=metric_size_sort%2Cdesc&p=0&m=&an=0",
    "eqix": "https://www.equinix.com/data-centers",
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


if __name__ == "__main__":
    # this is my stupid test suite, will remove and write as real unit tests sometime later
    async def main():
        browser = await uc.start()

        tab = await browser.get(
            "https://www.equinix.com/data-centers/asia-pacific-colocation/australia-colocation/brisbane-data-centers/br1"
        )
        df = await _eqix_scrape_single_property(tab)
        print("SCRAPED ONE ADDRESS LINE DF")
        print(df)
        print("\n\n\n")

        tab = await browser.get(
            "https://www.equinix.com/data-centers/americas-colocation/united-states-colocation/chicago-data-centers/ch2"
        )
        df = await _eqix_scrape_single_property(tab)
        print("SCRAPED TWO ADDRESS LINE DF")
        print(df)
        print("\n\n\n")

        tab = await browser.get("https://www.equinix.com/data-centers")
        print("SCRAPED CITY URLS")
        print(await _eqix_scrape_city_urls(tab))
        print("\n\n\n")

        tab = await browser.get(
            "https://www.equinix.com/data-centers/americas-colocation/canada-colocation/calgary-data-centers"
        )
        print("SCRAPED MULTIPLE PROPERTY URLS")
        print(await _eqix_scrape_single_city_property_urls(tab))
        print("\n\n\n")

        tab = await browser.get(
            "https://www.equinix.com/data-centers/asia-pacific-colocation/australia-colocation/brisbane-data-centers"
        )
        print("SCRAPED SINGLE PROPERTY URL")
        print(await _eqix_scrape_single_city_property_urls(tab))
        print("\n\n\n")

    uc.loop().run_until_complete(main())

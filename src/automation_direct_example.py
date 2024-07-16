"""Example script that scrapes data from automationdirect.com."""

# System imports
from __future__ import annotations

import csv
import logging
from pathlib import Path
from contextlib import contextmanager
from typing import TYPE_CHECKING

# Library imports
from selenium import webdriver
from selenium.webdriver.common.by import By

# Local imports
# Typing only imports
if TYPE_CHECKING:
    from collections.abc import Generator

logger = logging.getLogger(__name__)


@contextmanager
def chrome_driver() -> Generator[webdriver.Chrome, None, None]:
    """A context manager for a Chrome WebDriver instance."""
    # NOTE: We're wrapping this in a context manager so that the driver quits even if
    # an exception is raised.
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--start-maximized")
    # Optionally, keep the window open even after the script has finished execution.
    # Normally, I leave this commented unless I'm debugging.
    options.add_experimental_option("detach", value=True)

    # NOTE: we are using the network alias for the selenium-hub service defined in the
    # docker-compose file
    output_driver = webdriver.Remote(
        command_executor="http://selenium-hub:4444/wd/hub", options=options
    )

    try:
        # mypy seems to be confused about this type but it seems correct.
        yield output_driver # type: ignore[misc]
    finally:
        driver.quit()


with chrome_driver() as driver:
    driver.implicitly_wait(2)
    driver.get(
        "https://www.automationdirect.com/adc/shopping/catalog/drives_-a-_soft_starters"
        "/ac_variable_frequency_drives_(vfd)?_gl=1*1re5r94*_up*MQ..&"
        "gclid=Cj0KCQjwsuSzBhCLARIsAIcdLm44TEY-m6bEWDgfkV-PMHs741S4W2dGSIEaix9Ejl9MSRpG"
        "xf2H7-caApicEALw_wcB#Brand_Name_ms=%22WEG%20Electric%22&start=0"
    )

    # We need to click the "Agree" button on the cookies banner first so it doesn't
    # cover other content. Selenium will generally scroll to elements that you want to
    # interact with but this banner messes that up.
    COOKIES_BTN_XPATH = '//button[contains(@class,"cc-nb-okagree")]'
    driver.find_element(By.XPATH, COOKIES_BTN_XPATH).click()

    # Click the Table view option on the Automation Direct webpage.
    TABLE_VIEW_BTN_XPATH = '//a[contains(@title,"Table - Quick View")]'
    driver.find_element(By.XPATH, TABLE_VIEW_BTN_XPATH).click()

    # On one occasion, the selenium script started executing
    # before the webapge fully loaded.
    # In that rare case, I added a sleep time. There are better ways to do this.
    # time.sleep(1)

    product_table = driver.find_element(By.ID, "productListTable")

    # An empty array for stashing data we scrape.
    drive_data = []

    # https://stackoverflow.com/questions/27006698/selenium-iterating-through-groups-of-elements
    ROW_ELEMENTS_XPATH = '//div[contains(@class,"tableview rowentry")]'
    # row_element = driver.find_element(By.XPATH, ROW_ELEMENTS_XPATH)
    row_elements = product_table.find_elements(By.XPATH, ROW_ELEMENTS_XPATH)
    for row_element in row_elements:
        row_data = []

        product_name = row_element.find_element(
            By.XPATH, './/span[contains(@class,"itemcode-text")]'
        ).text
        row_data.append(product_name)

        product_price = row_element.find_element(
            By.XPATH, './/span[contains(@id,"price_d")]'
        ).text
        row_data.append(product_price)

        for product_attr in row_element.find_elements(
            By.XPATH, './/div[contains(@class,"dynamic-tr-attribute textEllipsis")]'
        ):
            attribute = product_attr.text
            # print('Attribute: {}'.format(attribute)) # print for debugging
            row_data.append(attribute)

        # print(row_data)
        drive_data.append(row_data)

    output_path = Path("build/output.csv")
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(drive_data)

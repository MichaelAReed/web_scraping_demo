"""Example script that scrapes data from automationdirect.com."""

# System imports
from __future__ import annotations

import logging

# Library imports
import requests
from bs4 import BeautifulSoup, element

# Local imports
# Typing only imports
# if TYPE_CHECKING:
#     from uuid import UUID

logger = logging.getLogger(__name__)

URL = 'https://www.automationdirect.com/adc/shopping/catalog/drives_-a-_soft_starters/ac_variable_frequency_drives_(vfd)#Brand_Name_ms="WEG%20Electric"&start=0'
headers = {
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, "
        "like Gecko) Chrome/102.0.0.0 Safari/537.36"
    ),
}

raw_page = requests.get(URL, headers=headers, timeout=5)
if raw_page.status_code != requests.status_codes.codes.ALL_OK:
    log_str = f"Failed to get page: {raw_page.status_code}"
    logger.error(log_str)
    raise requests.exceptions.HTTPError(log_str)

soup = BeautifulSoup(raw_page.content, "html.parser")

product_list_div = soup.find(id="productListTable")
if product_list_div is None or isinstance(product_list_div, element.NavigableString):
    log_str = "Failed to find product list div"
    raise ValueError(log_str)

product_entry_divs = product_list_div.find_all("div", class_="listview rowentry")

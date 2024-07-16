"""Example script that scrapes data from automationdirect.com."""

# System imports
from __future__ import annotations

import logging

# Library imports
from selenium import webdriver
from selenium.webdriver.common.by import By

# Local imports
# Typing only imports
# if TYPE_CHECKING:
#     from uuid import UUID

logger = logging.getLogger(__name__)


options = webdriver.ChromeOptions()
options.add_argument("--ignore-ssl-errors=yes")
options.add_argument("--ignore-certificate-errors")
driver = webdriver.Remote(
    command_executor="http://localhost:4444", options=options
)

driver.get("https://www.selenium.dev/selenium/web/web-form.html")

title = driver.title

driver.implicitly_wait(0.5)

text_box = driver.find_element(by=By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

text_box.send_keys("Selenium")
submit_button.click()

message = driver.find_element(by=By.ID, value="message")
text = message.text

driver.quit()

breakpoint()

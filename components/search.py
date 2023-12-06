import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec

from components.base import Base


class Search(Base):
    SEARCH_BAR_XPATH = f'//input[@data-testid="search-bar"]'
    SEARCH_BUTTON_XPATH = f'//button[@type="submit"]'

    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    def type(self, text: str):
        element = self.wait.until(ec.visibility_of_element_located((By.XPATH, self.SEARCH_BAR_XPATH)))
        element.send_keys(text)

    def paste(self, text: str):
        self.click(self.SEARCH_BAR_XPATH)
        ActionChains(self.driver).send_keys(text).send_keys(Keys.SHIFT, Keys.INSERT).perform()

    def press_return(self):
        element = self.wait.until(ec.visibility_of_element_located((By.XPATH, self.SEARCH_BAR_XPATH)))
        ActionChains(self.driver).move_to_element(element).send_keys(Keys.RETURN).perform()
        time.sleep(1)  # we are waiting for updated content

    def search_for(self, profile_name: str):
        self.type(profile_name)
        self.press_return()

    def click_button(self):
        self.click(self.SEARCH_BUTTON_XPATH)
import time


from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


class Base:
    SEARCH_BAR_XPATH = f'//input[@data-testid="search-bar"]'

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def click(self, xpath: str):
        self.wait.until(ec.element_to_be_clickable((By.XPATH, xpath))).click()

    def get_text(self, xpath: str):
        return self.wait.until(ec.presence_of_element_located((By.XPATH, xpath))).text

    def find_element(self, xpath: str):
        element = self.wait.until(ec.presence_of_element_located((By.XPATH, xpath)))
        time.sleep(0.2)
        return element

    def find_elements(self, item_xpath: str):
        self.wait.until(ec.presence_of_element_located(item_xpath))
        element = self.driver.find_elements(*item_xpath)
        return element

    def refresh_page(self):
        self.driver.refresh()
        self.wait.until(ec.element_to_be_clickable((By.XPATH, self.SEARCH_BAR_XPATH)))
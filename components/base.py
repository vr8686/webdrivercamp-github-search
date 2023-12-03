import time


from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


class Base:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def click(self, xpath: str):
        self.wait.until(ec.element_to_be_clickable((By.XPATH, xpath))).click()

    def get_text(self, xpath: str):
        return self.wait.until(ec.visibility_of_element_located((By.XPATH, xpath))).text

    def find_element(self, xpath: str):
        element = self.wait.until(ec.visibility_of_element_located((By.XPATH, xpath)))
        time.sleep(0.2)
        return element

    def get_attribute_text(self, xpath: str):
        element = self.find_element(xpath)
        element_url = element.get_attribute("href")
        return element_url

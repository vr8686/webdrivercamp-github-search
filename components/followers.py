from selenium.webdriver.common.by import By
from components.base import Base


class Followers(Base):
    FOLLOWER_XPATH = f'//div[@class="followers"]//article'
    FOLLOWERS_COMPONENT_XPATH = f'//article[@class="sc-hLBbgP cYMlzc"]'

    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    def get_followers(self):
        item_xpath = (By.XPATH, self.FOLLOWER_XPATH)
        followers = self.find_elements(item_xpath)
        return followers

    def get_follower_name(self, ancestor: str) -> str:
        name_xpath = f'{ancestor}//h4'
        return self.find_element(name_xpath).text

    def get_follower_link(self, ancestor: str) -> str:
        name_xpath = f'{ancestor}//a'
        return self.find_element(name_xpath).text

    def collect_followers_data(self):
        collected_data = {}
        followers_list = []
        followers_list.extend(item for item in self.get_followers())
        for i in range(1, len(followers_list) + 1):
            item_xpath = f'{self.FOLLOWER_XPATH}[{i}]'
            name = self.get_follower_name(item_xpath)
            link = self.get_follower_link(item_xpath)
            collected_data[name] = link
        return collected_data

    def check_followers_present(self):
        return self.find_element(self.FOLLOWERS_COMPONENT_XPATH)

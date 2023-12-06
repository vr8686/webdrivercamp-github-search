from components.base import Base


class User(Base):
    NAME_XPATH = f'//header//h4'
    TWITTER_XPATH = f'//header//p'
    BIO_XPATH = f'//p[@class="bio"]'
    COMPANY_XPATH = f'//div[@class="links"]//p[1]'
    LOCATION_XPATH = f'//div[@class="links"]//p[2]'
    BLOG_XPATH = f'//div[@class="links"]//a[@href]'
    USER_COMPONENT_XPATH = f'//article[@class="sc-dkrFOg bHWDWn"]'
    USER_COMPONENT_FOLLOW_LINK_XPATH = f'//header//a[contains(@href, "github")]'

    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    def get_name_ui(self):
        return self.get_text(self.NAME_XPATH)

    def get_twitter_ui(self):
        twitter = self.get_text(self.TWITTER_XPATH)
        # Replace each @ character with an empty string
        return twitter.replace('@', '')

    def get_bio_ui(self):
        return self.get_text(self.BIO_XPATH)

    def get_company_ui(self):
        return self.get_text(self.COMPANY_XPATH)

    def get_location_ui(self):
        return self.get_text(self.LOCATION_XPATH)

    def get_blog_ui(self):
        return self.get_text(self.BLOG_XPATH)

    def get_attribute_text(self):
        element = self.find_element(self.USER_COMPONENT_FOLLOW_LINK_XPATH)
        element_url = element.get_attribute("href")
        return element_url

    def get_data(self, data_type):
        method_mapping = {
            'name': self.get_name_ui,
            'company': self.get_company_ui,
            'blog': self.get_blog_ui,
            'location': self.get_location_ui,
            'bio': self.get_bio_ui,
            'twitter': self.get_twitter_ui
        }

        # Convert data type to lower case
        data_type = data_type.lower()

        # Check if the data type is in the method mapping
        if data_type in method_mapping:
            # Call the appropriate method and return the result
            return method_mapping[data_type]()
        else:
            # Handle the case where an invalid data type is provided
            raise ValueError(f"Invalid data type: {data_type}")

    def check_user_present(self):
        return self.find_element(self.USER_COMPONENT_XPATH)
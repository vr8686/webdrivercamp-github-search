from components.base import Base


class Summary(Base):
    REPOS_COUNT_XPATH = f'//div[contains(p, "repos")]//h3'
    FOLLOWERS_COUNT_XPATH = f'//div[contains(p, "followers")]//h3'
    FOLLOWING_COUNT_XPATH = f'//div[contains(p, "following")]//h3'
    GISTS_COUNT_XPATH = f'//div[contains(p, "gists")]//h3'

    def __init__(self, driver, wait):
        super().__init__(driver, wait)

    def get_repos_ui(self):
        return self.find_element(self.REPOS_COUNT_XPATH).text

    def get_followers_ui(self):
        return self.find_element(self.FOLLOWERS_COUNT_XPATH).text

    def get_following_ui(self):
        return self.find_element(self.FOLLOWING_COUNT_XPATH).text

    def get_gists_ui(self):
        return self.find_element(self.GISTS_COUNT_XPATH).text

    def get_data(self, data_type):
        method_mapping = {
            'repos': self.get_repos_ui,
            'followers': self.get_followers_ui,
            'following': self.get_following_ui,
            'gists': self.get_gists_ui,
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

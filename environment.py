from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def before_feature(context, feature):
    context.BASE_URL = f'https://gh-users-search.netlify.app/'
    context.BASE_API = f'https://api.github.com/'
    context.browser = webdriver.Chrome()
    context.browser.maximize_window()
    context.wait = WebDriverWait(context.browser, 5)


def after_scenario(context, scenario):
    context.browser.close()


def after_feature(context, feature):
    context.browser.quit()

# 123 test

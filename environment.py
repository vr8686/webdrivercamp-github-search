from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import helpers
from components.base import Base
from components.search import Search
from components.summary import Summary
from components.user import User
from components.followers import Followers


def before_feature(context, feature):
    context.BASE_URL = f'https://gh-users-search.netlify.app/'
    context.BASE_API = f'https://api.github.com/'
    context.browser = webdriver.Chrome()
    context.browser.maximize_window()
    context.wait = WebDriverWait(context.browser, 5)
    context.base = Base(context.browser, context.wait)
    context.search = Search(context.base.driver, context.base.wait)
    context.summary = Summary(context.base.driver, context.base.wait)
    context.user = User(context.base.driver, context.base.wait)
    context.followers = Followers(context.base.driver, context.base.wait)
    context.helpers = helpers


def after_step(context, step):
    print(f'STEP: {step.name} - {step.status}')


def after_scenario(context, scenario):
    print(f'SCENARIO: {scenario.name} - {scenario.status}')


def after_feature(context, feature):
    context.browser.close()

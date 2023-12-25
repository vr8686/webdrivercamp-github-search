from selenium import webdriver
from base.steps import api_steps
from base.environment import hooks


def before_all(context):
    hooks.before_all(context)


def before_feature(context, feature):
    hooks.before_feature(context, feature)
    context.BASE_URL = f'https://gh-users-search.netlify.app/'
    context.BASE_API = f'https://api.github.com'

    # Check if the @skip_browser tag is present in feature tags
    if 'skip_browser' not in feature.tags:
        context.browser = webdriver.Chrome()
        context.browser.maximize_window()


def before_scenario(context, scenario):
    hooks.before_scenario(context, scenario)


def before_step(context, step):
    hooks.before_step(context, step)


def after_step(context, step):
    hooks.after_step(context, step)


def after_scenario(context, scenario):
    hooks.after_scenario(context, scenario)


def after_feature(context, feature):
    hooks.after_feature(context, feature)

    # Check if the @skip_browser tag is present in feature tags
    if 'skip_browser' not in feature.tags:
        context.browser.quit()


def after_all(context):
    hooks.after_all(context)

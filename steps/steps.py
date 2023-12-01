from behave import *


@given('Navigate to GH-user-search')
def navigate_to_url(context):
    context.browser.get(context.BASE_URL)
    print('Navigating to https://gh-users-search.netlify.app/')


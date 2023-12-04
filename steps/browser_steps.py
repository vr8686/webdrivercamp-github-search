from behave import *


@given('Navigate to GH-user-search')
def navigate_to_url(context):
    context.browser.get(context.BASE_URL)
    print('Navigating to https://gh-users-search.netlify.app/')


@when("User enters {profile_name} in search field by {action}")
def step_impl(context, profile_name, action):
    if action == "typing":
        context.search.type(profile_name)
    elif action == "pasting":
        context.search.paste(profile_name)
    else:
        print('Action is not defined')
        raise ValueError


@step("User presses Return/Enter")
def step_impl(context):
    context.search.press_return()


@step("User clicks Search button")
def step_impl(context):
    context.base.click(context.SEARCH_BUTTON_XPATH)


@when('UI: search for {profile_name}')
def step_impl(context, profile_name):
    context.search.search_for(profile_name)

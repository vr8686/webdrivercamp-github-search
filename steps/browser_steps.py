from behave import *

import helpers
from components.base import Base
from components.search import Search
from components.summary import Summary


@given('Navigate to GH-user-search')
def navigate_to_url(context):
    context.browser.get(context.BASE_URL)
    print('Navigating to https://gh-users-search.netlify.app/')


@when("User enters {profile_name} in search field by {action}")
def step_impl(context, profile_name, action):
    search = Search(context.browser)
    if action == "typing":
        search.type(profile_name)
    elif action == "pasting":
        search.paste(profile_name)
    else:
        raise ValueError('Action is not defined')


@step("User presses Return/Enter")
def step_impl(context):
    search = Search(context.browser)
    search.press_return()


@step("User clicks Search button")
def step_impl(context):
    search = Search(context.browser)
    search.click_button()


@step('UI: search for {profile_name} with whitespace {position} it')
def step_impl(context, profile_name, position):
    # base = Base(context.browser, context.wait)
    search = Search(context.browser)
    profile_name_modified = helpers.add_whitespace(profile_name, position)
    print(f'Entering {profile_name_modified}')
    search.search_for(profile_name_modified)


@step('UI: search for {profile_name}')
def step_impl(context, profile_name):
    search = Search(context.browser)
    search.search_for(profile_name)


@step("collect data from Summary Component and store in context variable")
def step_impl(context):
    summary = Summary(context.browser)

    context.before_update = {}
    for row in context.table:
        data_type = row["Data Type"]
        ui_data = summary.get_data(data_type)
        context.before_update[data_type] = ui_data
    print(f'UI collected data before API update:\n{context.before_update}')


@then("UI: refresh page")
def step_impl(context):
    base = Base(context.browser)
    base.refresh_page()


@when("UI: enter whitespace into search field")
def step_impl(context):
    # base = Base(context.browser, context.wait)
    search = Search(context.browser)

    profile_name = " "
    search.type(profile_name)

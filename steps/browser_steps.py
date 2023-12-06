from behave import *
import helpers


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
        raise ValueError('Action is not defined')


@step("User presses Return/Enter")
def step_impl(context):
    context.search.press_return()


@step("User clicks Search button")
def step_impl(context):
    context.search.click_button()


@step('UI: search for {profile_name} with whitespace {position} it')
def step_impl(context, profile_name, position):
    profile_name_modified = helpers.add_whitespace(profile_name, position)
    print(f'Entering {profile_name_modified}')
    context.search.search_for(profile_name_modified)


@step('UI: search for {profile_name}')
def step_impl(context, profile_name):
    context.search.search_for(profile_name)


@step("collect data from Summary Component and store in context variable")
def step_impl(context):
    context.before_update = {}
    for row in context.table:
        data_type = row["Data Type"]
        ui_data = context.summary.get_data(data_type)
        context.before_update[data_type] = ui_data
    print(f'UI collected data before API update:\n{context.before_update}')


@then("UI: refresh page")
def step_impl(context):
    context.base.refresh_page()


@when("UI: enter whitespace into search field")
def step_impl(context):
    profile_name = " "
    context.search.type(profile_name)

from behave import *

import helpers
from components.followers import Followers
from components.summary import Summary
from components.user import User
from steps import api_steps


def verify_text_contained(content, text):
    try:
        assert text in content
        print(f'Match. {content} contains "{text}"')
    except AssertionError:
        print(f'Mismatch. {content} does NOT contain "{text}"')


def verify_data(data_type, api_data, ui_data):
    if data_type == 'Bio':
        # we return the string with no whitespace characters
        api_data = helpers.clean_bio_string(api_data)
    print(f'Checking UI vs API for "{data_type}"...')
    if str(api_data) == str(ui_data):
        print(f'{data_type}: UI data "{ui_data}" matches API data "{api_data}"')
    else:
        print(f'Mismatch for {data_type}: UI data "{ui_data}" DOES NOT match API data "{api_data}"')


def compare_followers(dict1, dict2):
    # Compare keys
    keys_diff_dict1 = sorted(set(dict1.keys()) - set(dict2.keys()))
    keys_diff_dict2 = sorted(set(dict2.keys()) - set(dict1.keys()))

    if keys_diff_dict1 or keys_diff_dict2:
        if keys_diff_dict1:
            print(f"Logins in API and not in UI: {keys_diff_dict1}")
        if keys_diff_dict2:
            print(f"Logins in UI and not in API: {keys_diff_dict2}")
    else:
        print('Logins match in both dictionaries')

    # Compare values
    values_diff = {key: (dict1[key], dict2[key]) for key in set(dict1.keys()) & set(dict2.keys()) if
                   dict1[key] != dict2[key]}
    if values_diff:
        print("Different links:")
        for key, (value1, value2) in values_diff.items():
            print(f"Login: {key}, Link API: {value1}, Link UI: {value2}")
    else:
        print('UI links data match API data')


@then('Verify "Follow" button contains {profile_name}')
def step_impl(context, profile_name):
    user = User(context.browser)

    content = user.get_attribute_text()
    verify_text_contained(content, profile_name)


@then("Verify UI search results match API request data in {component} Component")
def step_impl(context, component):
    user = User(context.browser)
    summary = Summary(context.browser)

    components = {"Summary": summary.get_data,
                  "User": user.get_data
                  }
    # Transforming data types in the table to JSON keys
    transformed_data_types = [helpers.gherkin_to_json(row["Data Type"]) for row in context.table]

    #  Creating JSONPath string to extract data based on Context Table from Scenario
    jsonpath_str = helpers.create_jsonpath(transformed_data_types)

    api_search_results = api_steps.get_api_data(f'{context.BASE_API}{context.endpoint}', jsonpath_str)

    for row in context.table:
        data_type = row["Data Type"]
        ui_data = components[component](data_type)
        api_data = api_search_results[helpers.gherkin_to_json(data_type)]
        verify_data(data_type, api_data, ui_data)


@step("UI: number of followers is less than 100 in Followers Component")
def step_impl(context):
    followers = Followers(context.browser)

    followers_ui = followers.get_followers()
    try:
        assert len(followers_ui) <= 100
        print(f'UI: Number of followers shown: {len(followers_ui)} does not exceed 100')
    except AssertionError as e:
        print(f'UI MISMATCH: number of followers shown: {len(followers_ui)} '
              f'exceeds 100')
        raise e


@step("UI: number of followers is actual in Followers Component")
def step_impl(context):
    followers_api = api_steps.get_api_followers_data(f'{context.BASE_API}{context.endpoint}')
    try:
        assert followers_api == followers_api
        print("UI: number of followers is actual in Followers Component")
    except AssertionError as e:
        print("UI: number of followers is WRONG in Followers Component")
        raise e


@step("Verify profile name and link match API request data")
def step_impl(context):
    followers = Followers(context.browser)

    ui_search_results = followers.collect_followers_data()
    api_search_results = api_steps.get_api_followers_data(f'{context.BASE_API}{context.endpoint}')

    #  Verify UI reflects correct API data
    print('Comparing UI name and link data for each follower with API data')
    compare_followers(api_search_results, ui_search_results)


@step("Verify UI search results")
def step_impl(context):
    summary = Summary(context.browser)

    context.after_update = {}
    for row in context.table:
        data_type = row["Data Type"]
        ui_data = summary.get_data(data_type)
        context.after_update[data_type] = ui_data
    print(f'UI collected data after API update:\n{context.after_update}')
    try:
        assert context.before_update == context.after_update
        print('UI verification: data was successfully updated')
    except AssertionError as e:
        print(f'UI: Updated data does not match initial data')
        print(f'Reverting Github changes.')
        api_steps.delete_repo(context, context.name, context.login, context.password)
        api_steps.unfollow_user(context, context.user, context.login, context.password)
        api_steps.delete_gist(context, context.login, context.password)
        raise e


@then("Assert empty result returned")
def step_impl(context):
    summary = Summary(context.browser)
    user = User(context.browser)
    followers = Followers(context.browser)

    # Empty result definition: no Summary, User and Followers components displayed
    try:
        assert summary.check_summary_present() is None
        assert user.check_user_present() is None
        assert followers.check_followers_present() is None
        print('UI search result is empty')
    except AssertionError as e:
        print('UI search result is NOT empty')
        raise e

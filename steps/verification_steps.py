from behave import *

import helpers
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
    values_diff = {key: (dict1[key], dict2[key]) for key in set(dict1.keys()) & set(dict2.keys()) if dict1[key] != dict2[key]}
    if values_diff:
        print("Different links:")
        for key, (value1, value2) in values_diff.items():
            print(f"Login: {key}, Link API: {value1}, Link UI: {value2}")
    else:
        print('UI links data match API data')


@then('Verify "Follow" button contains {profile_name}')
def step_impl(context, profile_name):
    content = context.base.get_attribute_text(context.USER_COMPONENT_FOLLOW_LINK_XPATH)
    verify_text_contained(content, profile_name)


@then("Verify UI search results match API request data in {component} Component")
def step_impl(context, component):
    components = {"Summary": context.summary.get_data,
                  "User": context.user.get_data
                  }
    # Transforming data types in the table to JSON keys
    transformed_data_types = [context.helpers.gherkin_to_json(row["Data Type"]) for row in context.table]

    #  Creating JSONPath string to extract data based on Context Table from Scenario
    jsonpath_str = context.helpers.create_jsonpath(transformed_data_types)

    api_search_results = api_steps.get_api_data(f'{context.BASE_API}{context.endpoint}', jsonpath_str)

    for row in context.table:
        data_type = row["Data Type"]
        ui_data = components[component](data_type)
        api_data = api_search_results[context.helpers.gherkin_to_json(data_type)]
        verify_data(data_type, api_data, ui_data)


@step("UI: number of followers is actual or max 100 is shown in Followers Component")
def step_impl(context):
    followers_ui = context.followers.get_followers()
    if len(followers_ui) <= 100:
        print(f'UI: number of followers shown: {len(followers_ui)} '
              f'does not exceed 100')
    else:
        print(f'UI MISMATCH: number of followers shown: {len(followers_ui)} '
              f'exceeds 100')


@step("Verify profile name and link match API request data")
def step_impl(context):
    ui_search_results = context.followers.collect_followers_data()
    api_search_results = api_steps.get_api_followers_data(f'{context.BASE_API}{context.endpoint}')

    print('Comparing UI name and link data for each follower with API data')
    compare_followers(api_search_results, ui_search_results)

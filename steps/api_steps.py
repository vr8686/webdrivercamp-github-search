import requests
from behave import *
from jsonpath_ng import parse


def send_get_request(url):
    print(f"Sending GET request to: {url}")
    r = requests.get(url, timeout=5)
    return r.status_code


def get_api_data(url: str, jsonpath_str: str):
    try:
        r = requests.get(url, timeout=5)
        assert r.status_code == 200

        # Deserializing data from HTTP request
        json_response = r.json()

        # Using jsonpath to extract specific data
        jsonpath = parse(jsonpath_str)
        matches = jsonpath.find(json_response)

        # Extracting values from matches
        result = {}
        for match in matches:
            # Accessing the last element of the path differently based on the type
            if isinstance(match.path, list):
                path = match.path[-1].value
            else:
                path = match.path

            result[str(path)] = match.value

        # print(f"Extracted user data: {result}")

        return result

    except AssertionError as e:
        print(f'Assertion Error - {e}')


def get_api_followers_data(url: str):
    try:
        r = requests.get(url, timeout=5)
        assert r.status_code == 200

        # Deserializing data from HTTP request
        json_response = r.json()

        # Define JSONPath expressions for "login" and "url"
        login_expr = parse("$.login")
        url_expr = parse("$.html_url")

        # Iterate through the array and create a dictionary {login: url}
        login_url_dict = {}
        for item in json_response:
            login = [match.value for match in login_expr.find(item)][0]
            url = [match.value for match in url_expr.find(item)][0]
            login_url_dict[login] = url

        # print(f"Extracted user data: {result}")

        return login_url_dict

    except AssertionError as e:
        print(f'Assertion Error - {e}')



@step("API: send GET request to {endpoint}")
def step_impl(context, endpoint):
    context.endpoint = endpoint
    try:
        response_code = send_get_request(f'{context.BASE_API}{endpoint}')
        assert response_code == 200
        print(f"Response status code: {response_code}")
    except AssertionError as e:
        print(f'Error occurred, response code is not 200. \n{e}')

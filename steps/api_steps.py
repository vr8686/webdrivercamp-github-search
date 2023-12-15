import requests
from behave import *
from jsonpath_ng import parse
from requests.auth import HTTPBasicAuth


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

        return login_url_dict

    except AssertionError as e:
        print(f'Assertion Error - {e}')


def check_if_follows(name: str, login: str, password: str):
    r = requests.get(f'https://api.github.com/user/following/{name}',
                     timeout=5,
                     auth=HTTPBasicAuth(login, password),
                     headers={
                         'Accept': 'application/vnd.github+json'
                     },
                     )
    print(f"Response status code: {r.status_code}")

    return r.status_code


def create_repo(name: str, login: str, password: str) -> dict:
    """
    Create a new repository on GitHub using the GitHub API.

    Returns:
    - dict: A dictionary with the JSON response from the GitHub API after creating the repository.
    """
    print(f'Creating a repo {name} for user {login}')

    r = requests.post('https://api.github.com/user/repos',
                      timeout=5,
                      auth=HTTPBasicAuth(login, password),
                      json={
                          "name": name,
                          'Accept': 'application/vnd.github+json'
                      },
                      )

    print(f"Response status code: {r.status_code}")

    if r.status_code == 201:
        print(f'Successfully created repo {name}')
    else:
        print(f'Failed to create repo {name}. Status code: {r.status_code}, Response: {r.text}')


def get_created_repo(name: str, login: str, password: str):
    """
    Retrieve details of a created repository from the given GitHub API URL.

    Raises:
    - AssertionError: If any of the assertions fail.
    """
    r = requests.get(f'https://api.github.com/repos/{login}/{name}',
                     timeout=5,
                     auth=HTTPBasicAuth(login, password),
                     json={'Accept': 'application/vnd.github+json'}
                     )
    print(f"Response status code: {r.status_code}")

    repo = r.json()

    # Asserting the repo was created with proper parameters
    if r.status_code != 404:
        try:
            assert repo['name'] == name
            assert repo['owner']['login'] == login
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


@then("API: create a repo {name} using {login} and {password}")
def step_impl(context, name, login, password):
    #  Storing data into context to use to revert changes if further verification fails
    context.name = name
    context.login = login
    context.password = password
    create_repo(name, login, password)
    get_created_repo(name, login, password)


@then("API: Delete repo {name} using {login} and {password}")
def delete_repo(context, name, login, password):
    """
        Delete a GitHub repository using the GitHub API.

        Note:
        - The function uses a DELETE request to delete the specified repository.
        """
    r = requests.delete(f'https://api.github.com/repos/{login}/{name}',
                        timeout=5,
                        auth=HTTPBasicAuth(login, password),
                        json={
                            "repo": name,
                            "owner": login,
                            'Accept': 'application/vnd.github+json'
                        },
                        )

    if r.status_code == 204:
        print(f'Successfully deleted repo {name}')
    else:
        print(f'Failed to delete repo {name}. Status code: {r.status_code}, Response: {r.text}')

    get_created_repo(name, login, password)


@step("API: follow {user} using {login} and {password}")
def step_impl(context, user, login, password):
    #  Storing data into context to use to revert changes if further verification fails
    context.user = user

    #  Checking if already following the user
    if check_if_follows(user, login, password) == 204:
        print(f'Already following {user}. Need to unfollow.')
        unfollow_user(context, user, login, password)
    print(f'API: following user {user}')

    r = requests.put(f'https://api.github.com/user/following/{user}',
                     timeout=5,
                     auth=HTTPBasicAuth(login, password),
                     json={
                         "username": user,
                         'Accept': 'application/vnd.github+json'
                     },
                     )

    if r.status_code == 204:
        print(f'Successfully followed user {user}')
    else:
        print(f'Failed to follow user {user}. Status code: {r.status_code}, Response: {r.text}')


@step("API: unfollow {user} using {login} and {password}")
def unfollow_user(context, user, login, password):
    print(f'Unfollowing user {user}')
    r = requests.delete(f'https://api.github.com/user/following/{user}',
                        timeout=5,
                        auth=HTTPBasicAuth(login, password),
                        headers={
                            'Accept': 'application/vnd.github+json'
                        },
                        )

    if r.status_code == 204:
        print(f'Successfully unfollowed user {user}')
    else:
        print(f'Failed to unfollow user {user}. Status code: {r.status_code}, Response: {r.text}')


@step("API: create a gist using {login} and {password}")
def step_impl(context, login, password):
    print(f'Creating a gist for user {login}')

    r = requests.post('https://api.github.com/gists',
                      timeout=5,
                      auth=HTTPBasicAuth(login, password),
                      json={
                          "description": 'test gist',
                          "files": {
                              'README.md': {
                                  "content": 'Hello World'
                              }
                          },
                          "public": True,
                          'Accept': 'application/vnd.github+json'
                      },
                      )

    print(f"Response status code: {r.status_code}")
    context.gist_id = r.json()['id']


@step("API: Delete created gist using {login} and {password}")
def delete_gist(context, login, password):
    print(f'Deleting a gist for user {login}')

    r = requests.delete(f'https://api.github.com/gists/{context.gist_id}',
                        timeout=5,
                        auth=HTTPBasicAuth(login, password),
                        json={
                            "gist_id": context.gist_id,
                            'Accept': 'application/vnd.github+json'
                        },
                        )

    if r.status_code == 204:
        print(f'Successfully deleted gist')
    else:
        print(f'Failed to deleted gist. Status code: {r.status_code}, Response: {r.text}')


@when("API: assert {invalid_user} does not exist on GitHub {login} and {password}")
def step_impl(context, invalid_user, login, password):
    r = requests.get(f'https://api.github.com/users/{invalid_user}',
                     timeout=5,
                     auth=HTTPBasicAuth(login, password),
                     headers={
                         'Accept': 'application/vnd.github+json'
                     },
                     )
    try:
        assert r.status_code == 404
        print(f'The user {invalid_user} does not exist.')
    except AssertionError as e:
        print(f'The user {invalid_user} exist on Github. Please choose another user.')
        raise e

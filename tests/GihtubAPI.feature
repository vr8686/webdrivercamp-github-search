@skip_browser
Feature: GitHub API testing

  Scenario: Get all repos
    When send GET request to search/repositories
      | webdrivercamp-learning-python |
    Then verify status code is 200
    And verify Number of repos is 23

  Scenario: Get repo with authentication
    When send GET request with authentication to user/repos
    Then verify status code is 200
    And verify Number of repos is 0

  Scenario: Create Repo
    Given clear JSON data in payload
    When add values to payload
      | name     | repo-created-with-api |
      | private  | True                  |
      | has_wiki | False                 |
    And send POST request with authentication to user/repos
    Then verify status code is 201

  Scenario Outline: Get created Repo
    When send GET request with authentication to repos/<login>/<repo>
    Then verify status code is 200
    And verify parameters
      | login    | trainingprofile       |
      | name     | repo-created-with-api |
      | private  | True                  |
      | has_wiki | False                 |
    Examples:
      | login           | repo                  |
      | trainingprofile | repo-created-with-api |

  Scenario Outline: Update created Repo
    Given clear JSON data in payload
    When add values to payload
      | description | I know Python Requests! |
    And Send PATCH request with authentication to repos/<login>/<repo>
    Then verify status code is 200
    And verify parameters
      | description | I know Python Requests! |
    Examples:
      | login           | repo                  |
      | trainingprofile | repo-created-with-api |

  Scenario Outline: Delete Repo
    When Send DELETE request with authentication to repos/<login>/<repo>
    Then verify status code is 204
    Examples:
      | login           | repo                  |
      | trainingprofile | repo-created-with-api |

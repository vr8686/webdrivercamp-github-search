Feature: GHUS-Search

  Background: User opens main page
    Given Navigate to GH-user-search

  Scenario Outline: Verify search can be started with Enter/Return
    When User types <login> in search field
    And User presses Return/Enter
    Then Verify name in the User Component is <name>
    Examples:
    #  <login> and <name> as named in github API JSON response
      | login  | name   |
      | google | Google |


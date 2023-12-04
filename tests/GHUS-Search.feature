Feature: GHUS-Search

  Background: User opens main page
    Given Navigate to GH-user-search

  Scenario Outline: Verify search can be started with Enter/Return
    When User enters <profile_name> in search field by <action>
    And User presses Return/Enter
      #  search is completed if "follow" link contains <profile_name> we searched for
    Then Verify "Follow" button contains <profile_name>
    Examples:
      | action  | profile_name |
      | typing  | google       |
      | pasting | apple        |

  Scenario Outline: Verify search can be started by clicking on the Search button
    When User enters <profile_name> in search field by <action>
    And User clicks Search button
      #  search is completed if "follow" link contains <profile_name> we searched for
    Then Verify "Follow" button contains <profile_name>
    Examples:
      | action  | profile_name |
      | typing  | google       |
      | pasting | apple        |

  Scenario Outline: Verify search results reflect actual data in Summary Component
    When UI: search for <profile name>
    And API: send GET request to users/<profile name>
    Then Verify UI search results match API request data in Summary Component
      | Data Type |
      | Repos     |
      | Followers |
      | Following |
      | Gists     |
    Examples:
      | profile name |
      | blister      |

  Scenario Outline: Verify search results reflect actual data in User Component
    When UI: search for <profile name>
    And API: send GET request to users/<profile name>
    Then Verify UI search results match API request data in User Component
      | Data Type |
      | Name      |
      | Company   |
      | Blog      |
      | Location  |
      | Bio       |
      | Twitter   |
    And Verify "Follow" button contains <profile name>
    Examples:
      | profile name |
      | blister      |

  Scenario Outline: Verify search results reflect actual data in Followers Component
    When UI: search for <profile name>
    And API: send GET request to users/<profile name>/followers?per_page=100
    Then UI: number of followers is actual or max 100 is shown in Followers Component
    And Verify profile name and link match API request data
    Examples:
      | profile name |
      | blister      |

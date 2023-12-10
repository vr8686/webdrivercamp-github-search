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

  Scenario Outline: Verify search results reflect actual data in Summary Component - data exists
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

  Scenario Outline: Verify search results reflect actual data in Summary Component - no data
    # We use a dummy account - "trailingprofile" with 0 repos, followers, followings and gists
    When UI: search for <profile name>
    And API: send GET request to users/<profile name>
    Then Verify UI search results match API request data in Summary Component
      | Data Type |
      | Repos     |
      | Followers |
      | Following |
      | Gists     |
    Examples:
      | profile name    |
      | trainingprofile |

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
    Then UI: number of followers is actual in Followers Component
    And Verify profile name and link match API request data
    Examples:
      | profile name |
      | blister      |

  Scenario Outline: Verify search results show no more than 100 followers in Followers Component
    When UI: search for <profile name>
    And API: send GET request to users/<profile name>/followers?per_page=100
    Then UI: number of followers is less than 100 in Followers Component
    And Verify profile name and link match API request data
    Examples:
      | profile name |
      | blister      |

  Scenario Outline: Verify UI data is updated after changes made on Github side
    # We use a dummy account - "trailingprofile" with 0 repos, followers, followings and gists
    When UI: search for <profile name>
    And collect data from Summary Component and store in context variable
      | Data Type |
      | Repos     |
      | Following |
      | Gists     |
    Then API: create a repo <repo name> using <profile name> and <password>
    And API: follow <profile to follow> using <profile name> and <password>
    And API: create a gist using <profile name> and <password>
    Then UI: refresh page
    And Verify UI search results
      | Data Type |
      | Repos     |
      | Following |
      | Gists     |
    Then API: Delete repo <repo name> using <profile name> and <password>
    And API: Unfollow <profile to follow> using <profile name> and <password>
    And API: Delete created gist using <profile name> and <password>
    Examples:
      | profile name    | password                                 | profile to follow | repo name |
      | trainingprofile | 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 | vr8686            | test-repo |

  Scenario Outline: Verify number of followers (UI) is updated after changes made on Github side
#    When UI: search for <profile to follow>
#    And collect data from Summary Component and store in context variable
#      | Data Type |
#      | Followers |
#    And API: follow <profile to follow> using <profile name> and <password>
#    Then UI: refresh page
#    And Verify UI search results
#      | Data Type |
#      | Followers |
    And API: Unfollow <profile to follow> using <profile name> and <password>
    Examples:
      | profile name    | password                                 | profile to follow |
      | trainingprofile | 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 | vr8686            |

  Scenario Outline: Verify not valid username populates an empty result
    When API: assert <invalid user> does not exist on GitHub <profile name> and <password>
    And UI: search for <invalid user>
    Then Assert empty result returned
    Examples:
      | invalid user   | profile name    | password                                 |
      | fdjfkjsflsglsg | trainingprofile | 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 |

  Scenario: Verify an empty result is returned when entering no data
    When User presses Return/Enter
    Then Assert empty result returned

  Scenario: Verify an empty result is returned when entering no data
    When User clicks Search button
    Then Assert empty result returned

  Scenario: Verify an empty result is returned when entering username modified with whitespaces
    When UI: enter whitespace into search field
    Then Assert empty result returned

  Scenario Outline: Verify an empty result is returned when entering username modified with whitespaces
    When UI: search for <profile name> with whitespace <position> it
    Then Assert empty result returned
    Examples:
      | profile name | position |
      | vr8686       | before   |
      | vr8686       | after    |
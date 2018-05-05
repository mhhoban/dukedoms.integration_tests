@game_invite_flows
Feature: Game Invitation Flows

Background: Test DB with only one account
  Given an empty account database
  And an empty game service database
  When account service receives request for new account with details:
    | email          |
    | test@test.test |

Scenario: Create Game, Send Invite, Accept Invite
  When account service receives request for new account with details:
    | email              |
    | test_one@test.test |
  And game service receives request to create new game with properties:
    | host_player    | invited_players    |
    | test@test.test | test_one@test.test |
  Then the game service successfully creates a new game
  And account service shows that player "test@test.test" has joined the game
  And player "test_one@test.test" receives an invite to the game
  When player "test_one@test.test" "accepts" the game invitation
  Then the game service shows that player "test_one@test.test" has "accepted" the invite
  And the account service shows that player "test_one@test.test" has "accepted" the invite

  @foo
  Scenario: Create Game, Send Invite, Accept Invite, End Turn
    When account service receives request for new account with details:
      | email              |
      | test_one@test.test |
    And game service receives request to create new game with properties:
      | host_player    | invited_players    |
      | test@test.test | test_one@test.test |
    Then the game service successfully creates a new game
    And account service shows that player "test@test.test" has joined the game
    And player "test_one@test.test" receives an invite to the game
    When player "test_one@test.test" "accepts" the game invitation
    Then the game service shows that player "test_one@test.test" has "accepted" the invite
    And the account service shows that player "test_one@test.test" has "accepted" the invite
    When game service is queried for player id for player "test@test.test"
    And game service is queried for player id for player "test_one@test.test"
    Then game service returns an id
    When player service is queried for turn phase for player "test@test.test"
    Then player service returns turn phase "action"
    When game service receives request to end turn for player "test@test.test"
    And player service is queried for turn phase for player "test@test.test"
    Then player service returns turn phase "inactive"
    When player service is queried for turn phase for player "test_one@test.test"
    Then player service returns turn phase "action"


Scenario: Create Game, Send Invite, Decline Invite
  When account service receives request for new account with details:
    | email              |
    | test_one@test.test |
  And game service receives request to create new game with properties:
    | host_player | invited_players    |
    | blarg       | test_one@test.test |
  Then the game service successfully creates a new game
  And player "test_one@test.test" receives an invite to the game
  When player "test_one@test.test" "declines" the game invitation
  Then the game service shows that player "test_one@test.test" has "declined" the invite
  And the account service shows that player "test_one@test.test" has "declined" the invite

@game_service
Feature: Game Service

Background: Test DB with only one account
  Given an empty game service database
  When account service receives request for new account with details:
    | email          |
    | test@test.test |

  Scenario: Create New Game
    When game service receives request to create new game with properties:
    | host_player | invited_players |
    | blarg       | targ,plarg      |
    Then the game service successfully creates a new game
    When game service receives request for that game info
    Then the game service returns a game with info:
    | host_player| invited_players | game_status| pending_players |
    | blarg      | targ,plarg     | pending    | targ,plarg       |

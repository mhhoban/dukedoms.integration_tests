@game_service
Feature: Game Service

  Scenario: Create New Game
    When service receives request to create new game with properties:
    | host_player | invited_players |
    | blarg       | targ, plarg     |
    Then the game service successfully creates a new game
    When service receives request for that game info
    Then the game service returns a game with info:
    | host_player| invited_players | game_status| pending_players |
    | blarg      | targ, plarg     | pending    | targ, plarg     |

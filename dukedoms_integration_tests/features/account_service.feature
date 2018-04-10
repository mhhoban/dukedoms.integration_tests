@account_service
Feature: Account Service

  Background: Test DB with only one account
    Given an empty account database
    When account service receives request for new account with details:
      | email          |
      | test@test.test |

  Scenario: Test Account Creation
    When account service receives request for new account with details:
      | email              |
      | test_one@test.test |
    And account service is queried with the new account id
    Then account service returns accounts with info
      | email              |
      | test_one@test.test |

  Scenario: Test retrieve multiple account ids
    When account service receives request for new account with details:
      | email              |
      | test_one@test.test |
    And account service is queried for account ids for email addresses:
      | email              |
      | test_one@test.test |
      | test@test.test     |
    Then account service returns the account ids for those email addresses
    When account service is queried with the account ids it returned
    Then account service returns accounts with info
      | email              |
      | test_one@test.test |
      | test@test.test     |

  Scenario: Get Account Id By Email Address
    When account service receives request for account id for email address:
      | email          |
      | test@test.test |
    Then the account service returns an id
    When account service receives another request for account id for email address:
      | email         |
      | test@test.test|
    Then the account service returns the same id

  Scenario: Verify Account Exists
    When account service receives request for account validation for:
      | email          |
      | test@test.test |
    Then account service returns True

  Scenario: Verify Account Does Not Exist
    When account service receives request for account validation for:
      | email               |
      | test_fail@test.test |
    Then account service returns False

  Scenario: Verify Accounts Exist
    When account service receives request for new account with details:
      | email           |
      | test2@test.test |
    And account service receives request for account validation for:
      | email           |
      | test@test.test  |
      | test2@test.test |
    Then account service returns True

  Scenario: Verify Accounts Do Not Exist
    When account service receives request for account validation for:
      | email                   |
      | test_fail_one@test.test |
      | test_fail_two@test.test |
    Then account service returns validation failure object with:
      | email                   |
      | test_fail_one@test.test |
      | test_fail_two@test.test |

  @foo
  Scenario: Add Game Invite Notification
    When account service receives request to invite player to game:
      | player email   | game id |
      | test@test.test | 13      |
    And account service receives request for account id for email address:
      | email          |
      | test@test.test |
    Then account service shows game id when queried for player invites:
      | player email   | game id |
      | test@test.test | 13      |

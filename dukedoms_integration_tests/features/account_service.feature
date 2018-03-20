Feature: Account Service

  Scenario: Create Account
  Given an empty account database
  When account service receives request for new account with details:
  | email          |
  | test@test.test |
  Then the request is successful
  When account service receives request for account id for email address:
  | email          |
  | test@test.test |
  Then we receive an account id
  

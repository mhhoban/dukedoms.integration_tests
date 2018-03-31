
from behave import given, then, when
from hamcrest import assert_that, equal_to, is_not
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

@given('an empty account database')
def clear_account_service_db(context):
    """
    drop any existing information from tables for a clean test run.
    """
    engine = create_engine(context.env_urls.account_service_db)
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()
    session.execute('TRUNCATE table accounts')
    session.close()

@when('account service receives request for new account with details')
def step_new_account(context):
    """
    attempt to create a new account
    """
    for row in context.table:
        account_request = context.clients.account_service.get_model('NewAccountRequest')(
            email=row['email']
        )

        result, status = context.clients.account_service.newAccount.create_new_account(
            newAccountRequest=account_request
        ).result()

        assert_that(status.status_code, equal_to(200))
        assert_that(result.account_id, is_not(None))

        context.account_id = result.account_id

@when('account service is queried with the new account id')
def step_query_service_with_id(context):
    """
    get account info from account id
    """
    result, status = context.clients.account_service.accountInfo.get_player_info(
        accountId=context.account_id
    ).result()

    assert_that(status.status_code, equal_to(200))

    context.account_email = result.email

@then('it returns account with info')
def assert_account_info_correct(context):
    """
    verify expected account info returned
    """
    for row in context.table:
        assert_that(context.account_email, equal_to(row['email']))

@when('account service receives request for account id for email address')
def step_get_id_for_email(context):
    """
    query account service for the ids corresponding to given emails
    """
    account_emails = [row['email'] for row in context.table]

    result, status = context.clients.account_service.accountInfo.get_account_ids(
        requestedAccounts=account_emails
    ).result()
    assert_that(status.status_code, equal_to(200))
    context.account_ids = result

@then('the account service returns an id')
def assert_account_id(context):
    """
    Gherkin placeholder for a step in the story
    """
    assert_that(context.account_ids, is_not(None))

@when('account services receives another request for account id for email address')
def step_get_account_id_again(context):
    account_emails = [row['email'] for row in context.table]

    result, status = context.clients.account_service.accountInfo.get_account_ids(
        requestedAccounts=account_emails
    ).result()
    assert_that(status.status_code, equal_to(200))
    context.second_account_ids = result

@then('the account service returns the same id')
def assert_account_ids_identical(context):
    assert_that(
        context.second_account_ids[0],
        equal_to(context.account_ids[0])
    )

@when('account service receives request for account validation for')
def step_request_account_validation(context):
    """
    send account service request to validate given email is signed up
    """
    player_list = [row['email'] for row in context.table]
    result, status = context.clients.account_service.accountInfo.verify_accounts(
        playerList=player_list
    )

    context.request_status_code = status.status_code

@then('account service returns True')
def assert_accounts_valid(context):
    assert_that(context.request_status_code, equal_to(200))


@then('account service returns False')
def assert_accounts_valid(context):
    assert_that(context.request_status_code, equal_to(404))

@when('account service receives request to invite player to game id:')
def step_invite_players(context):
    """
    send the invitation for a set of players to be invited to a game to
    account service
    """
    invitation_batch = context.clients.account_service.get_model('InvitationBatch')(
        gameId=context.table.rows[0]['game id'],
        playerList=[row['player'] for row in context.table]
    )
    result, status = context.clients.account_service.gameOperations.invite_accounts(
        invitationBatch=invitation_batch
    )
    assert_that(status.status_code, equal_to(202))

@when('account services shows game id when queried for player invites')
def assert_player_invite_successful(context):
    account_emails = [email for row['player email'] in context.table]

    result, status = context.clients.account_service.accountInfo.get_account_ids(
        requestAccountIds=account_emails
    )
    assert_that(status.status_code, equal_to(200))
    account_id = result[0]

    result, status = context.clients.account_service.accountInfo.get_player_info(
        accountId=account_id
    )
    assert_that(status.status_code, equal_to(200))

    expected_game_id = context.table.rows[0]['game id']
    assert_that(result.gameInvitations[0], equal_to(expected_game_id))

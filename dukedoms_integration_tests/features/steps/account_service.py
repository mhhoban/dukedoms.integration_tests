from behave import given, then, when
from bravado.exception import HTTPNotFound
from hamcrest import assert_that, equal_to, is_not, greater_than, has_item
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

    session.execute('TRUNCATE TABLE accounts')
    session.commit()
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

        context.new_account_id = [result.account_id]

@when('account service is queried with the new account id')
def step_query_new_account_id(context):
    """
    get account info for new account id
    """

    result, status = context.clients.account_service.accountInfo.get_player_info(
        accountIds=context.new_account_id
    ).result()

    assert_that(status.status_code, equal_to(200))
    context.returned_accounts = result.player_accounts

@when('account service is queried with the account ids it returned')
def step_query_service_with_ids(context):
    """
    get account info from account id
    """

    account_ids = [list(dict.values())[0] for dict in context.account_id_mappings]

    result, status = context.clients.account_service.accountInfo.get_player_info(
        accountIds=account_ids
    ).result()

    assert_that(status.status_code, equal_to(200))
    context.returned_accounts = result.player_accounts

@then('account service returns accounts with info')
def assert_account_info_correct(context):
    """
    verify expected account info returned
    """
    verify_player_info(context.table.rows, context.returned_accounts)

@when('account service receives request for account id for email address')
@when('account service is queried for account ids for email addresses')
def step_get_id_for_email(context):
    """
    query account service for the ids corresponding to given emails
    """
    account_emails = [row['email'] for row in context.table]

    result, status = context.clients.account_service.accountInfo.get_account_ids(
        requestedAccounts=account_emails
    ).result()
    assert_that(status.status_code, equal_to(200))

    context.account_id_mappings = result.accountIdMappings

@then('account service returns the account ids for those email addresses')
@then('the account service returns an id')
def assert_account_id(context):
    """
    Gherkin placeholder for a step in the story
    """
    assert_that(context.account_id_mappings, is_not(None))

@when('account service receives another request for account id for email address')
def step_get_account_id_again(context):
    account_emails = [row['email'] for row in context.table]

    result, status = context.clients.account_service.accountInfo.get_account_ids(
        requestedAccounts=account_emails
    ).result()

    assert_that(status.status_code, equal_to(200))
    context.second_account_id = result.accountIdMappings

@then('the account service returns the same id')
def assert_account_ids_identical(context):

    assert_that(context.account_id_mappings, equal_to(context.second_account_id))

@when('account service receives request for account validation for')
def step_request_account_validation(context):
    """
    send account service request to validate given email is signed up
    """
    player_list = [row['email'] for row in context.table]

    result, status = context.clients.account_service.accountInfo.verify_accounts(
        playerList=player_list
    ).result()

    context.verification_request_response = result

@then('account service returns True')
def assert_accounts_valid(context):
    assert_that(len(context.verification_request_response.unverified_players), equal_to(0))


@then('account service returns False')
def assert_accounts_valid(context):
    assert_that(len(context.verification_request_response.unverified_players), greater_than(0))

@when('account service receives request to invite player to game')
def step_invite_players(context):
    """
    send the invitation for a set of players to be invited to a game to
    account service
    """
    invitation_batch = context.clients.account_service.get_model('InvitationBatch')(
        gameId=int(context.table.rows[0]['game id']),
        playerList=[row['player email'] for row in context.table]
    )
    result, status = context.clients.account_service.gameOperations.invite_accounts(
        invitationBatch=invitation_batch
    ).result()
    assert_that(status.status_code, equal_to(202))

@then('account service shows game ids when account "{acct_email}" is queried for game invites')
def assert_player_invite_successful(context, acct_email):
    account_emails = list(acct_email)

    result, status = context.clients.account_service.accountInfo.get_player_info(
        accountIds=list(context.account_id_mappings[0].values())
    ).result()
    assert_that(status.status_code, equal_to(200))

    #helper function to compare expected vs received game gameInvitations
    expected_games = [int(row['game id']) for row in context.table]
    received_games = result.player_accounts[0]['game_invitations']['game_invitation_ids']
    compare_game_invitations(
        expected_games=expected_games,
        received_games=received_games
    )

    expected_game_id = context.table.rows[0]['game id']

    assert_that(result.player_accounts[0]['game_invitations']['game_invitation_ids'][0], equal_to(int(expected_game_id)))

@then('account service returns validation failure object with')
def assert_player_validation_failures(context):
    for player in [row['email'] for row in context.table]:
        assert_that(context.verification_request_response.unverified_players, has_item(player))

def verify_player_info(table, accounts):
    """
    verify that specified info is accounted for in returned account data
    """
    specified_emails = [row['email'] for row in table]
    returned_emails = [account['email'] for account in accounts]

    for email in specified_emails:
        assert_that(returned_emails, has_item(email))

    return True

def compare_game_invitations(expected_games=None, received_games=None):
    """
    compare expected to received_games
    """
    for game in expected_games:
        assert_that(received_games, has_item(game))
    return True

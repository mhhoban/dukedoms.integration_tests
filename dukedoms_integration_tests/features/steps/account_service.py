from behave import given, then, when
from hamcrest import assert_that, equal_to, is_not

@given('an empty account database')
def clear_account_service_db:
    """
    drop any existing information from tables for a clean test run.
    """
    engine = create_engine(context.env_urls.account_service_db)
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()
    session.execute('DROP * from account')
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
        assert_that(result.account_id is_not(None))

        context.account_id = result.account_id

@when('acount service is queried with the new account id')
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
    account_emails = [email for row['email'] in context.table]

    result, status = context.clients.account_service.accountInfo.get_account_ids(
        requestAccountIds=account_emails
    )
    assert_that(status.status_code, equal_to(200))
    context.account_ids = result

@then('the account service returns an id')
def assert_account_id(context):
    """
    Gherkin placeholder for a step in the story
    """
    assert_that(context.get_account_ids, is_not(None))

@when('account services receives another request for account id for email address')
def step_get_account_id_again(context):
    account_emails = [email for row['email'] in context.table]

    result, status = context.clients.account_service.accountInfo.get_account_ids(
        requestAccountIds=account_emails
    )
    assert_that(status.status_code, equal_to(200))
    context.second_account_ids = result

@then('the account service returns the same id')
def assert_account_ids_identical(context):
    assert_that(
        context.second_account_ids[0].playerId,
        equal_to(context.account_ids[0].playerId)
    )

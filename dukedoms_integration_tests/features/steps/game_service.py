from behave import given, then, when
from hamcrest import assert_that, equal_to, contains_inanyorder, is_in, has_item
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

@given('an empty game service database')
def clear_account_service_db(context):
    """
    drop any existing information from tables for a clean test run.
    """
    engine = create_engine(context.env_urls.game_service_db)
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()

    session.execute('TRUNCATE TABLE games')
    session.commit()
    session.close()

@when('game service is queried for player id for player "{player_email}"')
def get_player_id(context, player_email):
    player_id, status = context.clients.game_service.gameInfo.get_player_id(
        gameId=context.game_id,
        playerEmail=player_email
    ).result()
    context.player_ids[player_email] = player_id['playerId']

@when('game service receives request to end turn for player "{player_email}"')
def send_end_turn_request(context, player_email):
    result, status = context.clients.game_service.gameOperations.end_player_turn(
        endTurnRequest={
            'gameId': context.game_id,
            'playerEmail': player_email
        }
    ).result()


def create_new_game_request(client=None, invited_player_list=None, host_player=None, host_player_id=None):
    """
    Creates and returns new_game_request object
    """
    invited_players = {"invitedPlayers": invited_player_list}
    new_game_object = client.get_model('NewGameRequest')(
        hostPlayer=host_player,
        hostPlayerId=host_player_id,
        invitedPlayers=invited_players
    )

    return new_game_object

@when('game service receives request to create new game with properties')
def step_create_game(context):
    """
    Create a new game with game service
    """
    for row in context.table:
        host_player = row['host_player']
        new_game_request = create_new_game_request(
            client=context.clients.game_service,
            host_player=host_player,
            host_player_id=int(context.account_ids[host_player]),
            invited_player_list=row['invited_players'].split(',')
        )
        results, status = context.clients.game_service.gameOperations.create_new_game(
            newGameRequest=new_game_request
        ).result()

        assert_that(status.status_code, equal_to(200))
        context.status_code = status.status_code
        context.game_id = results.game_id

@then('the game service successfully creates a new game')
def assert_game_created(context):
    assert_that(context.status_code, equal_to(200))

@then('game service returns an id')
@when('game service receives request for that game info')
def step_request_game_info(context):
    pass

@then('the game service returns a game with info')
def assert_game_info(context):
    results, status = context.clients.game_service.getGame.get_game_info(
        gameId=context.game_id
    ).result()

    assert_that(context.table.rows[0]['host_player'], equal_to('blarg'))

    for player in context.table.rows[0]['invited_players'].split(','):
        assert_that(player, is_in(results.players['invited_players']['invitedPlayers']))

@then('the game service shows that player "{player_email}" has "{invite_response}" the invite')
def assert_game_service_shows_invite(context, player_email, invite_response):
    results, status = context.clients.game_service.gameInfo.get_game_info(
        gameId=context.game_id
    ).result()
    assert_that(
        len(results.players['pending_players']['pendingPlayers']),
        equal_to(0)
    )

    if invite_response == 'accepted':
        assert_that(
            results.players['accepted_players']['acceptedPlayers'],
            has_item(player_email)
        )
    else:
        assert_that(
            results.players['declined_players']['declinedPlayers'][0],
            equal_to(player_email)
        )

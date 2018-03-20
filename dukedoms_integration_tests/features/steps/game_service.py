from behave import given, then, when
from hamcrest import assert_that, equal_to, contains_inanyorder, is_in

#def create_new_game_request(client, host_player, invited_players):
def create_new_game_request(client=None, invited_players=None, host_player=None):
    """
    Creates and returns new_game_request object
    """
    invited_players = {"invitedPlayers": invited_players}
    host_player = host_player
    new_game_object = client.get_model('NewGameRequest')(
        hostPlayer=host_player,
        invitedPlayers=invited_players
    )

    return new_game_object

@when('service receives request to create new game with properties')
def step_create_game(context):
    """
    Create a new game with game service
    """
    for row in context.table:
        new_game_request = create_new_game_request(
            client=context.clients.game_service,
            host_player=row['host_player'],
            invited_players=row['invited_players'].split(',')
        )
        results, status = context.clients.game_service.newGame.create_new_game(
            newGameRequest=new_game_request
        ).result()

        assert_that(status.status_code, equal_to(200))
        context.status_code = status.status_code
        context.game_id = results.game_id

@then('the game service successfully creates a new game')
def assert_game_created(context):
    assert_that(context.status_code, equal_to(200))

@when('service receives request for that game info')
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

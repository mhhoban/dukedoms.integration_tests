from behave import given, then, when

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


    new_game_request = create_new_game_request(
        client=context.clients.game_service,
        host_player='blarg',
        invited_players=['blarg, targ']
    )
    results, status = context.clients.game_service.newGame.create_new_game(
        newGameRequest=new_game_request
    ).result()

@then('the game service successfully creates a new game')
def assert_game_created(context):
    pass

@when('service receives request for that game info')
def step_request_game_info(context):
    pass

@then('the game service returns a game with info')
def assert_game_info(context):
    pass

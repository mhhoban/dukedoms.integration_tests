from behave import given, then, when
from hamcrest import assert_that, equal_to, contains_inanyorder, is_in, has_item


@when('player service is queried for turn phase for player "{player_email}"')
def query_player_service(context, player_email):
    player_id = context.player_ids[player_email]
    player_info, status = context.clients.player_service.playerInfo.get_player_info(
        playerId=player_id
    ).result()
    context.player_info = player_info

@then('player service returns turn phase "{phase}"')
def assert_player_phase(context, phase):
    assert_that(
        context.player_info['turn_phase'],
        equal_to(phase)
    )

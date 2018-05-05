import os

from addict import Dict
from bravado.client import SwaggerClient
from bravado.swagger_model import load_file

def get_environment_variables(env):

    URLS = Dict()
    URLS.local.game_service = 'http://localhost:5003'
    URLS.local.dukedoms_rdbs = 'http://localhost:5432'
    URLS.local.account_service = 'http://localhost:5002'
    URLS.local.player_service = 'http://localhost:5004'
    URLS.local.account_service_db = 'postgresql+psycopg2://postgres:daleria@127.0.0.1:5432/account_service'
    URLS.local.game_service_db = 'postgresql+psycopg2://postgres:daleria@127.0.0.1:5432/game_service'

    URLS.container.game_service = 'game-service:5003'
    URLS.container.account_service = 'account-service:5002'
    URLS.container.player_service = 'player-service:5004'
    URLS.container.dukedoms_rdbs = 'dukedoms-rdbs:5432'
    URLS.container.account_service_db = 'postgresql+psycopg2://dukedoms:daleria@dukedoms-rdbs:5432/account_service'

    if env == 'local':
        return URLS.local
    else:
        return URLS.container

def before_scenario(context, step):

    context.account_ids = {}
    context.player_ids = {}

    config = {
        'also_return_response': True,
        'validate_responses': True,
        'validate_requests': True,
        'validate_swagger_spec': True,
        'use_models': True,
        'formats': []
    }

    env = context.config.userdata.get('env')
    context.env_urls = get_environment_variables(env)
    context.clients = Dict()
    context.clients.game_service = SwaggerClient.from_spec(
        load_file(
            'specs/dukedoms_game_service_api.yaml',
        ),
        origin_url=context.env_urls.game_service,
        config=config
    )

    context.clients.account_service = SwaggerClient.from_spec(
        load_file(
            'specs/dukedoms_account_service_api.yaml',
        ),
        origin_url=context.env_urls.account_service,
        config=config
    )

    context.clients.player_service = SwaggerClient.from_spec(
        load_file(
            'specs/dukedoms_player_service_api.yaml',
        ),
        origin_url=context.env_urls.player_service,
        config=config
    )

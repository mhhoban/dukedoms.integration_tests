import os

from addict import Dict
from bravado.client import SwaggerClient
from bravado.swagger_model import load_file

def get_environment_variables(env):

    URLS = Dict()
    URLS.local.game_service = 'http://localhost:5000'
    URLS.local.dukedoms_rdbs = 'http://localhost:5001'

    URLS.container.game_service = 'game-service:5000'
    URLS.container.dukedoms_rdbs = 'dukedoms-rdbs:5432'

    if env == 'local':
        return URLS.local
    else:
        return URLS.container

def before_step(context, step):

    config = {
        'also_return_response': True,
        'validate_responses': True,
        'validate_requests': True,
        'validate_swagger_spec': True,
        'use_models': True,
        'formats': []
    }

    env = os.environ.get('TEST_ENV')
    context.env_urls = get_environment_variables(env)
    context.clients = Dict()
    context.clients.game_service = SwaggerClient.from_spec(
        load_file(
            'specs/game_service_spec.yaml',
        ),
        origin_url=context.env_urls.game_service,
        config=config
    )

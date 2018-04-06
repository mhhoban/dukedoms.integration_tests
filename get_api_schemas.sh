#!/bin/bash

curl https://raw.githubusercontent.com/mhhoban/dukedoms.game_service_api/master/dukedoms_game_service_api.yaml -O
curl https://raw.githubusercontent.com/mhhoban/dukedoms.account_service_spec/master/dukedoms_account_service_api.yaml -O

mv dukedoms_game_service_api.yaml dukedoms_integration_tests/specs/dukedoms_game_service_api.yaml
mv dukedoms_account_service_api.yaml dukedoms_integration_tests/specs/dukedoms_account_service_api.yaml

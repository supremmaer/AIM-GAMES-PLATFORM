release: python AIM_GAMES_PLATFORM/manage.py migrate

release: python AIM_GAMES_PLATFORM/manage.py create_groups

web: sh -c 'cd AIM_GAMES_PLATFORM && gunicorn AIM_GAMES_PLATFORM.wsgi --log-file -'

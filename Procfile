release: python AIM_GAMES_PLATFORM/manage.py migrate ; python AIM_GAMES_PLATFORM/manage.py create_groups ; python AIM_GAMES_PLATFORM/manage.py populate

web: sh -c 'cd AIM_GAMES_PLATFORM && gunicorn AIM_GAMES_PLATFORM.wsgi --log-file -'

release: python AIM_GAMES_PLATFORM/manage.py migrate

web: sh -c 'cd AIM_GAMES_PLATFORM && gunicorn AIM_GAMES_PLATFORM.wsgi --log-file -'

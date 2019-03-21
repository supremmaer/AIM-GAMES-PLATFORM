release: python AIM_GAMES_PLATFORM/manage.py makemigrations

release: python AIM_GAMES_PLATFORM/manage.py migrate

release: python AIM_GAMES_PLATFORM/manage.py graph_models --pydot -a -g -o AIM_GAMES_PLATFORM/staticfiles/model.png

web: sh -c 'cd AIM_GAMES_PLATFORM && gunicorn AIM_GAMES_PLATFORM.wsgi --log-file -'

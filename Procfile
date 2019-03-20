<<<<<<< HEAD
model: python AIM_GAMES_PLATFORM/manage.py graph_models --pydot -a -g -o model.png

release: python AIM_GAMES_PLATFORM/manage.py migrate
=======
release: python AIM_GAMES_PLATFORM/manage.py makemigrations
>>>>>>> a318becc7407517db3c22d1897f4ec54c029c0d1

release: python AIM_GAMES_PLATFORM/manage.py migrate

<<<<<<< HEAD
=======
release: python AIM_GAMES_PLATFORM/manage.py graph_models --pydot -a -g -o model.png
>>>>>>> a318becc7407517db3c22d1897f4ec54c029c0d1

web: sh -c 'cd AIM_GAMES_PLATFORM && gunicorn AIM_GAMES_PLATFORM.wsgi --log-file -'

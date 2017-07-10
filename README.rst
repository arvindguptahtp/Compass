Student Support Generator
=========================

CIS network search tool.

Quickstart
----------

This application is distributed using Docker and Docker Compose. This means *nothing* for the application is installed directly on your host system.

1. Ensure you have Docker installed. The easiest way to run Docker on macOS is using `the desktop installer <https://www.docker.com/docker-mac>`_.
2. Update your `.env` file to ensure it includes this line `COMPOSE_FILE=dev.yml`. This ensures Docker Compose will use the dev configuration for setting up the system.
3. Run `docker-compose up` to download, build, and bring up the containers for the first time.
4. If you want to stop the development servers run `docker-compose down`. You will need to run this from a different terminal pane but from the same project root.

Because all commands are run *through* the containers, you must specify the containers you want to execute commands in. Docker Compose adds some porcelain to this:

    docker-compose run django python manage.py makemigrations

This command executes the `run` subcommand, targetting the container identified by Docker
Compose as the `django` container, and then executes the command given.

This is still verbose for common tasks, so the `dj.sh` convenience script can be used instead
as a wrapper to the above Docker Composer command:

    ./dj.sh makemigraions

Tests can be run using a make command:

    make test

See the 'Docker' section below for more information about using Docker and Docker Compose.

Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ ./dj.sh createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html


Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd network_search
    celery -A network_search.taskapp worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.


Deployment
----------

The following details how to deploy this application.


Heroku
^^^^^^

See detailed `cookiecutter-django Heroku documentation`_.

.. _`cookiecutter-django Heroku documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html



Docker
^^^^^^

Use Docker Compose as your interface to working with the Docker containers.

The Makefile includes several small convenience commands, including:

    make build

Which rebuilds the Docker images. This is a necessary step if you make changes to
requirements.

    make test

This runs the tests.

    make format

This runs the autoformatting commands inside the Django container.

    make run

This is an alias to the `up` command to bring up the Docker container cluster.

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html


Front-end
^^^^^^^^^

All front-end code is developed in the `front-end` directory. However, commands are run from the 
general Makefile at project root. Various development commands are broken out in the Makefile to 
speed up development compilation time. In general, look at the Makefile for all the 
various commands.

Before commit and deployment:

    make ui-build

This command compiles all needed template files, JavaScript, and CSS. It minifies the 
Javascript and CSS files and run the CSS files through CSS Razor, which removes all non-used
style declarations. This keeps the JS and CSS lean and fast for transmission and browser rendering.


Initial development session:

    make ui-dev

Ui-dev rebuilds the whole asset chain and watches all development files. The compilation/render 
is slow as the CSS libraries are sizeable. As `make ui-build` minifies and razors the asset files, 
this command is needed to activate all available style declarations and JS code. Use this command
if you are doing some small quick development updates or to start a longer development session.

Continued development session:

    make dev

Dev watches and compiles only the template files and the `app.styl` specific Stylus CSS (therefore, any code
not within the `_base` directory). Results in quicker development compilation cycles. Run `make ui-dev` once, 
`Ctrl-C` the process after initial build is complete, and then run `make dev`.

Javascript development:

    make vue-dev

Vue-dev centers on `.vue` and `.js` files only. This frees up compilation cycles as the watcher is only looking at the files
specifically included. All JS development should happen under this Make command.


** Always remember to run `make ui-build` before an expected deployment. **

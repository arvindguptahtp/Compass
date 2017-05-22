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

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ py.test


Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd network_search
    celery -A network_search.taskapp worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.





Sentry
^^^^^^

Sentry is an error logging aggregator service. You can sign up for a free account at  https://sentry.io/signup/?code=cookiecutter  or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.


Deployment
----------

The following details how to deploy this application.


Heroku
^^^^^^

See detailed `cookiecutter-django Heroku documentation`_.

.. _`cookiecutter-django Heroku documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html



Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html



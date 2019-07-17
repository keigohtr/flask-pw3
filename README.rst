The Flask-PW3
##############

.. _badges:

.. .. image:: http://img.shields.io/travis/keigohtr/flask-pw3.svg?style=flat-square
    .. :target: http://travis-ci.org/keigohtr/flask-pw3
    .. :alt: Build Status

.. .. image:: http://img.shields.io/pypi/v/flask-pw3.svg?style=flat-square
    .. :target: https://pypi.python.org/pypi/flask-pw3
    .. :alt: Version

.. .. image:: http://img.shields.io/pypi/dm/flask-pw3.svg?style=flat-square
    .. :target: https://pypi.python.org/pypi/flask-pw3
    .. :alt: Downloads

.. _description:

Forked from https://github.com/klen/flask-pw , can be used with peewee 3.x.


The Flask-PW3 -- Peewee_ ORM intergration for Flask_ framework.

The plugin configures DB connection and provides some tools such as migrations
and signals. It also provides Peewee_ ORM support for Flask-Debugtoolbar_

.. _contents:

.. contents::

Requirements
=============

- python 2.7+,3.4+
- peewee 3+

.. _installation:

Installation
=============

**Flask-PW3** should be installed using pip: ::

    pip install flask-pw3

.. _usage:

Usage
=====

Settings
--------

Flask-PW3 settings (default values): ::

    # Connection URI (FlaskDB)
    DATABASE = 'sqlite:///peewee.sqlite'

    # Path to directory which contains migrations
    PEEWEE_MIGRATE_DIR = 'migrations'

    # Name of database table with migrations
    PEEWEE_MIGRATE_TABLE = 'migratehistory'

    # Path to module which contains you applications' Models
    # Needed by automatic migrations
    PEEWEE_MODELS_MODULE = ''

    # Models which should be ignored in migrations
    PEEWEE_MODELS_IGNORE = []

    # Base models class
    # Use `db.Model` as your models' base class for automatically DB binding 
    PEEWEE_MODELS_CLASS = <flask_pw.Model>

    # Don't connect to db when request starts and close when it ends automatically
    PEEWEE_MANUAL = False


Example
-------

::

    import peewee as pw
    from flask import Flask

    from flask_pw import Peewee


    app = Flask(__name__)

    app.config['DATABASE'] = 'sqlite:///:memory:'

    db = Peewee(app)


    class User(db.Model):

        name = pw.CharField(255)
        title = pw.CharField(127, null=True)
        active = pw.BooleanField(default=True)
        rating = pw.IntegerField(default=0)


    @User.post_save.connect
    def update(user, created=False):
        if created:
            # Do something


Migrations
----------

If you use `Flask-Script` just add 'db' command to your manager: ::

    manager = Manager(create_app)
    manager.add_command('db', db.manager)

And use `db create`, `db migrate` and `db rollback` commands.

If you use `Flask >= 0.11` connect the plugin's command to your CLI: ::

    pw = Peewee(app)
    app.cli.add_command(pw.cli, 'db')


::

    if __name__ == '__main__':
        with app.app_context():
            app.cli()



Flask-Debugtoolbar
------------------

Just add `flask_pw.debugtoolbar.PeeweeDebugPanel` to Flask-Debugtoolbar_ panels in your
application's configuration: ::

    DEBUG_TB_PANELS = [
        'flask_debugtoolbar.panels.versions.VersionDebugPanel',
        'flask_debugtoolbar.panels.timer.TimerDebugPanel',
        'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask_debugtoolbar.panels.template.TemplateDebugPanel',
        'flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel',
        'flask_debugtoolbar.panels.logger.LoggingPanel',
        'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',

        # Add the Peewee panel
        'flask_pw.flask_debugtoolbar.PeeweeDebugPanel',
    ]

Enjoy!


.. _bugtracker:

Bug tracker
===========

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/keigohtr/flask-pw3/issues

.. _contributing:

Contributing
============

Development of The Flask-pw3 happens at: https://github.com/keigohtr/flask-pw3


Contributors
=============

* `Kirill Klenov <https://github.com/klen>`_

.. _license:

License
========

Licensed under a MIT license (See LICENSE)

.. _links:

.. _Flask: http://flask.pocoo.org/
.. _Peewee: http://docs.peewee-orm.com/en/latest/

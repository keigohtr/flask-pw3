import logging
from importlib import import_module

import peewee as pw
from cached_property import cached_property
from flask._compat import string_types
from peewee_migrate.router import Router
from playhouse.db_url import connect
from playhouse.flask_utils import FlaskDB

from .models import Model, BaseSignalModel, Choices # noqa


__license__ = "MIT"
__project__ = "Flask-PW3"
__version__ = "0.1.0a2"

LOGGER = logging.getLogger(__name__)


class Peewee(FlaskDB):

    def __init__(self, app=None, database=None, model_class=Model):
        super(Peewee, self).__init__(app, database, model_class)

    def init_app(self, app):
        super(Peewee, self).init_app(app)

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['peewee'] = self

        app.config.setdefault('PEEWEE_MANUAL', False)
        app.config.setdefault('PEEWEE_MIGRATE_DIR', 'migrations')
        app.config.setdefault('PEEWEE_MIGRATE_TABLE', 'migratehistory')
        app.config.setdefault('PEEWEE_MODELS_CLASS', Model)
        app.config.setdefault('PEEWEE_MODELS_IGNORE', [])
        app.config.setdefault('PEEWEE_MODELS_MODULE', '')
        app.config.setdefault('PEEWEE_READ_SLAVES', '')
        app.config.setdefault('PEEWEE_USE_READ_SLAVES', True)

    @property
    def models(self):
        """Return self.application models."""
        Model_ = self._app.config['PEEWEE_MODELS_CLASS']
        ignore = self._app.config['PEEWEE_MODELS_IGNORE']

        models = []
        if Model_ is not Model:
            try:
                mod = import_module(self._app.config['PEEWEE_MODELS_MODULE'])
                for model in dir(mod):
                    models = getattr(mod, model)
                    if not isinstance(model, pw.Model):
                        continue
                    models.append(models)
            except ImportError:
                return models
        elif isinstance(Model_, BaseSignalModel):
            models = BaseSignalModel.models

        return [m for m in models if m._meta.name not in ignore]

    def cmd_create(self, name, auto=False):
        """Create a new migration."""

        LOGGER.setLevel('INFO')
        LOGGER.propagate = 0

        router = Router(self.database,
                        migrate_dir=self._app.config['PEEWEE_MIGRATE_DIR'],
                        migrate_table=self._app.config['PEEWEE_MIGRATE_TABLE'])

        if auto:
            auto = self.models

        router.create(name, auto=auto)

    def cmd_migrate(self, name=None, fake=False):
        """Run migrations."""
        from peewee_migrate.router import Router, LOGGER

        LOGGER.setLevel('INFO')
        LOGGER.propagate = 0

        router = Router(self.database,
                        migrate_dir=self._app.config['PEEWEE_MIGRATE_DIR'],
                        migrate_table=self._app.config['PEEWEE_MIGRATE_TABLE'])

        migrations = router.run(name, fake=fake)
        if migrations:
            LOGGER.warn('Migrations are completed: %s' % ', '.join(migrations))

    def cmd_rollback(self, name):
        """Rollback migrations."""
        from peewee_migrate.router import Router, LOGGER

        LOGGER.setLevel('INFO')
        LOGGER.propagate = 0

        router = Router(self.database,
                        migrate_dir=self._app.config['PEEWEE_MIGRATE_DIR'],
                        migrate_table=self._app.config['PEEWEE_MIGRATE_TABLE'])

        router.rollback(name)

    def cmd_list(self):
        """List migrations."""
        from peewee_migrate.router import Router, LOGGER

        LOGGER.setLevel('DEBUG')
        LOGGER.propagate = 0

        router = Router(self.database,
                        migrate_dir=self._app.config['PEEWEE_MIGRATE_DIR'],
                        migrate_table=self._app.config['PEEWEE_MIGRATE_TABLE'])

        LOGGER.info('Migrations are done:')
        LOGGER.info('\n'.join(router.done))
        LOGGER.info('')
        LOGGER.info('Migrations are undone:')
        LOGGER.info('\n'.join(router.diff))

    def cmd_merge(self):
        """Merge migrations."""
        from peewee_migrate.router import Router, LOGGER

        LOGGER.setLevel('DEBUG')
        LOGGER.propagate = 0

        router = Router(self.database,
                        migrate_dir=self._app.config['PEEWEE_MIGRATE_DIR'],
                        migrate_table=self._app.config['PEEWEE_MIGRATE_TABLE'])

        router.merge()

    @cached_property
    def manager(self):
        """Integrate a Flask-Script."""
        from flask_script import Manager, Command

        manager = Manager(usage="Migrate database.")
        manager.add_command('create', Command(self.cmd_create))
        manager.add_command('migrate', Command(self.cmd_migrate))
        manager.add_command('rollback', Command(self.cmd_rollback))
        manager.add_command('list', Command(self.cmd_list))
        manager.add_command('merge', Command(self.cmd_merge))

        return manager

    @cached_property
    def cli(self):
        import click

        @click.group()
        def cli():
            """Peewee Migrations."""
            from flask import current_app

            if self._app is None:
                self.init_app(current_app)

        @cli.command()
        @click.argument('name')
        @click.option('--auto', is_flag=True)
        def create(name, auto=False):
            """Create a new migration."""
            return self.cmd_create(name, auto)

        @cli.command()
        @click.argument('name', default=None, required=False)
        @click.option('--fake', is_flag=True)
        def migrate(name, fake=False):
            """Run migrations."""
            return self.cmd_migrate(name, fake)

        @cli.command()
        @click.argument('name')
        def rollback(name):
            """Rollback migrations."""
            return self.cmd_rollback(name)

        @cli.command()
        def list():
            """List migrations."""
            return self.cmd_list()

        return cli


def get_database(obj, **params):
    """Get database from given URI/Object."""
    if isinstance(obj, string_types):
        return connect(obj, **params)
    return obj

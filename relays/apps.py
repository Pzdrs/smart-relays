from django.apps import AppConfig
from django.db import connections, DEFAULT_DB_ALIAS
from django.db.migrations.executor import MigrationExecutor


class RelaysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relays'
    audit_log_pagination_page_size = 10

    def ready(self):
        from . import signals

        if not self.__has_unapplied_migrations():
            from smart_relays.models import ApplicationData
            from relays.utils.gpio import init_GPIO
            ApplicationData.objects.get_or_create(
                key='setup_wizard',
                defaults={'data': {'completed': False, 'step': 0}}
            )
            #init_GPIO()

    def __has_unapplied_migrations(self):
        executor = MigrationExecutor(connections[DEFAULT_DB_ALIAS])
        targets = executor.loader.graph.leaf_nodes()
        plan = executor.migration_plan(targets)
        for migration in plan:
            if str(migration[0]).split('.')[0] == self.name:
                return True
        return False

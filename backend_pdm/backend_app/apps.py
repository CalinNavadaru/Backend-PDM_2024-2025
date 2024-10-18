from django.apps import AppConfig
from django.core.signals import request_finished
from django.db import close_old_connections
from . import scheduler
class BackendAppConfig(AppConfig):
    name = 'backend_app'

    def ready(self):
        scheduler.start()

        request_finished.connect(close_old_connections)

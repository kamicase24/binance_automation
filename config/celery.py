import os
from celery import Celery
from django.apps import apps, AppConfig
from django.conf import settings
    
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
# if not settings.configured:
app = Celery('core')
app.config_from_object("django.conf:settings", namespace="CELERY")
    
class CeleryConfig(AppConfig):
    name = 'binance_automation.celery'
    verbose_name = 'Configuración de App para Celery'

    def ready(self):
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)





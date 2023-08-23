from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "binance_automation.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import binance_automation.users.signals  # noqa F401
        except ImportError:
            pass

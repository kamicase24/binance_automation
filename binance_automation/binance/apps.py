from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BinanceConfig(AppConfig):
    name = "binance_automation.binance"
    verbose_name = _("Binance Base model")

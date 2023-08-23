from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from binance_automation.binance.models.account import BinanceAccount
from import_export.admin import ExportActionMixin



@admin.register(BinanceAccount)
class BinanceAccountAdmin(ExportActionMixin, admin.ModelAdmin):

    search_fields = [
        'name',
        'code',
        'secret',
        'api_key',
    ]

    list_filter = [
        'name',
        'code',
        'secret',
        'api_key',
    ]

    list_display = [
        'name',
        'code',
        'secret',
        'api_key',
    ]
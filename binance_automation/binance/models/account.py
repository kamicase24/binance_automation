"""Binance Account Model"""
from django.db import models
from binance_automation.utils.models import BinanceAutomationModel
import logging
from binance.spot import Spot
from datetime import datetime, timedelta

class BinanceAccount(BinanceAutomationModel):

    name = models.CharField(verbose_name='Cuenta', max_length=120, blank=False, null=False)
    code = models.CharField(verbose_name='Código de cuenta', max_length=120, blank=False, null=False, unique=True)
    api_key = models.CharField(verbose_name='API Key', max_length=240, blank=True, null=True)
    secret = models.CharField(verbose_name='Secret Key', max_length=240, blank=True, null=True)


    def get_binance_client(self):
        return Spot(api_key=self.api_key, api_secret=self.secret)


    def get_futures_transfer_history(self, asset='USDT', history_date=datetime.now()):
        client = self.get_binance_client()
        timestamp_in_seconds = (history_date - datetime(1970, 1, 1)).total_seconds()
        timestamp_in_milliseconds = int(timestamp_in_seconds * 1000)
        res = client.futures_transfer_history(asset, startTime=timestamp_in_milliseconds)
        return res

    def __str__(self):
        return f'{self.id}'


    class Meta(BinanceAutomationModel.Meta):

        db_table = 'binance_automation'
        verbose_name_plural = 'Cuentas Binance'

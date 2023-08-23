from django.views.generic.base import View
from django.shortcuts import render, redirect, get_object_or_404
from binance_automation.binance.forms.account import BinanceAccountForm
from binance_automation.binance.models.account import BinanceAccount
from datetime import datetime, timedelta
import logging


class BinanceAccountViewSet(View):
    template_name = 'binance/account.html'

    def get(self, request):
        form = BinanceAccountForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = BinanceAccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, self.template_name, {'form': form})

class BinanceAccountDeleteView(View):
    
    def get(self, request, binance_account_id):
        binance_account_id = get_object_or_404(BinanceAccount, id=binance_account_id)
        binance_account_id.delete()
        return redirect('/')
    
class BinanceAccountFutTraHisView(View):
    template_name = 'binance/future_transfer_history.html'

    def get(self, request, binance_account_id):
        binance_account_id = BinanceAccount.objects.get(id=binance_account_id)
        history_date = datetime.now() - timedelta(hours=24)
        res = binance_account_id.get_futures_transfer_history('USDT', history_date)
        logging.info(res)
        return render(request, self.template_name, res)

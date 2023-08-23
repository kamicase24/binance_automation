from django.urls import include, path

from binance_automation.binance.views.account import (
    BinanceAccountDeleteView, BinanceAccountFutTraHisView,
    BinanceAccountViewSet)

urlpatterns = [
    path('account/', BinanceAccountViewSet.as_view(), name='binance_account'),
    path('account/delete/<int:binance_account_id>', BinanceAccountDeleteView.as_view(), name='delete_binance_account'),
    path('account/futures_transfer_history/<int:binance_account_id>', BinanceAccountFutTraHisView.as_view(), name='futures_transfer_history')
]

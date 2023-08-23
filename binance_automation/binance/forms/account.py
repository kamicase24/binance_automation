from django import forms
from binance_automation.binance.models.account import BinanceAccount

class BinanceAccountForm(forms.ModelForm):
    class Meta:
        model = BinanceAccount
        fields = ['name', 'code', 'secret', 'api_key']
        labels = {
            'name': 'Cuenta',
            'code': 'Código de cuenta',
            'secret': 'Secret Key',
            'api_key': 'API Key',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'label': 'Cuenta'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'label': 'Código'}),
            'secret': forms.PasswordInput(render_value=True, 
                                          attrs={'class': 'form-control', 'label': 'Secret Key'}),
            'api_key': forms.PasswordInput(render_value=True, 
                                          attrs={'class': 'form-control', 'label': 'API Key'}),
        }

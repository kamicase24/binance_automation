from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from binance_automation.users.forms.auth import CustomLoginForm
from binance_automation.binance.models.account import BinanceAccount
import logging

def login_home(request):
    form = CustomLoginForm()
    data = {'form': form, 'binance_account_ids': BinanceAccount.objects.all()}
    if request.method == 'POST':
        user = request.POST.get('login', None)
        password = request.POST.get('password', None)
        user = authenticate(username=user.lower(), password=password)
        if user is None:
            logging.error('Correo o contraseña incorrectos')
            data.update(login_error='Correo o contraseña incorrectos')
        else:
            if user.is_active:
                login(request, user)
            else:
                logging.error('Usuario inactivo')
                data.update(login_error='Usuario inactivo')

    return render(request, 'pages/home.html', data)
from django.shortcuts import render, redirect
from django.contrib.messages import constants
from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse

from usuarios.forms import RegisterForm

# Cadastrando um usuario
def cadastro(request):
    form = RegisterForm()
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            auth.login(request, usuario)
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso!')
            return redirect('usuarios:cadastro')
    return render(request,'cadastro.html', {'form': form})

# Autenticando um usuario
def logar(request):
    form = AuthenticationForm(request)
    if request.POST:
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.add_message(request, constants.SUCCESS, 'Login realizado com sucesso!')
            return redirect('/')
        messages.add_message(request, constants.ERROR,'Login inválido')
    return render(request, 'login.html', {'form': form})
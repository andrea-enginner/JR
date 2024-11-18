from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

from apps.registro.models import Vendedor
from .forms import UsuarioCreationForm

from django.shortcuts import redirect

def pagina_inicial(request):
    """
    Redireciona para a página de login.
    """
    return redirect('/login/')



def register(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Cria o vendedor se o checkbox estiver marcado
            if user.is_vendedor:
                Vendedor.objects.create(usuario=user)
            # Autentica e loga o usuário
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = UsuarioCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Recupera o email do formulário
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)  # Autenticação por email
        if user:
            login(request, user)
            return redirect('home')  # Redireciona para a página inicial
        else:
            return render(request, 'registration/login.html', {'error': 'Credenciais inválidas. Por favor, tente novamente.'})
    return render(request, 'registration/login.html')
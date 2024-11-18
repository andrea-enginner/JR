from django import views
from django.shortcuts import render
from django.urls import path
from .views import pagina_inicial, register, login_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', pagina_inicial, name='pagina_inicial'),  
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', lambda request: render(request, 'home.html'), name='home'),  
    # Página inicial
]

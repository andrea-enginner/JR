from django.shortcuts import render
from django.urls import path
from django import views

from .views import deletar_produto_view, editar_produto_view, meus_produtos, minhas_avaliacoes, pagina_inicial, register, login_view, cadastrar_produto
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', pagina_inicial, name='pagina_inicial'),  
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', lambda request: render(request, 'home.html'), name='home'),  
    # Página inicial
    path('cadastrar_produto/', cadastrar_produto, name='cadastrar_produto'), 
    path('meus_produtos/', meus_produtos, name='meus_produtos'),
    path('minhas_avaliacoes/', minhas_avaliacoes, name='minhas_avaliacoes'),
    path('produto/editar/<int:id>/', editar_produto_view, name='editar_produto'),
    path('produto/deletar/<int:id>/', deletar_produto_view, name='deletar_produto'),
]

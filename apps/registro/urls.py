from django.shortcuts import render
from django.urls import path

from apps.registro.views import ProdutoViewSet, alterar_senha, chat, deletar_produto_view, editar_perfil, editar_produto_view, meu_perfil, meus_produtos, minhas_avaliacoes, obter_mensagens, pagina_inicial, produto_comprar_view, produto_detalhes_view, register, login_view, cadastrar_produto
from django.contrib.auth.views import LogoutView

from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from registro.models import Chat

# Registrar os ViewSets
router = DefaultRouter()
router.register(r'products', ProdutoViewSet, basename='product')

urlpatterns = [
    path('', pagina_inicial, name='pagina_inicial'),  
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', lambda request: render(request, 'home.html'), name='home'),  

#   AÇÕES DO USUÁRIO COM SEUS PRODUTOS
    path('cadastrar_produto/', cadastrar_produto, name='cadastrar_produto'), 
    path('meus_produtos/', meus_produtos, name='meus_produtos'),
    path('minhas_avaliacoes/', minhas_avaliacoes, name='minhas_avaliacoes'),
    path('produto/editar/<int:id>/', editar_produto_view, name='editar_produto'),
    path('produto/deletar/<int:id>/', deletar_produto_view, name='deletar_produto'),


#   vizualização do produto e compra
    path('produto/<int:produto_id>/', produto_detalhes_view, name='produto_detalhes'),

    path('produto/<int:produto_id>/comprar/', produto_comprar_view, name='produto_comprar'),


#   AÇÕES DO USUÁRIO COM SEU PERFIL
    path('meu-perfil/', meu_perfil, name='meu_perfil'), 
    path('editar-perfil/', editar_perfil, name='editar_perfil'),
    path('alterar-senha/', alterar_senha, name='alterar_senha'),
    path('logout-message/', TemplateView.as_view(template_name='registration/logout_pass.html'), name='logout_message'),
    # Perfil do usuário
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Recuperação de senha

    # Chat
    path('chat/<int:produto_id>/', chat, name='chat'),
    path('mensagens/<int:produto_id>/', obter_mensagens, name='obter_mensagens'),


    #----------------------------API

    path('api/', include(router.urls)),  # Inclui as rotas criadas pelo router
]

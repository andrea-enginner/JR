from django.urls import path
from . import views  # Certifique-se de importar as views corretamente

urlpatterns = [
    path('lanches/', views.marketplace_view, name='marketplace'),  # Defina a view para a rota principal
]

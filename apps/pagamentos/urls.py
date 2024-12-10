from django.urls import path
from .views import listar_webhooks, mercadopago_webhook

urlpatterns = [
    path('webhook/', mercadopago_webhook, name='mercadopago_webhook'),
    path('listar-webhooks/', listar_webhooks, name='listar_webhooks'),
]

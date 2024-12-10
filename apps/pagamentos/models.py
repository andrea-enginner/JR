from django.db import models

class WebhookLog(models.Model):
    tipo = models.CharField(max_length=50, blank=True, null=True)  # Tipo do webhook (ex.: "payment")
    dados = models.JSONField()  # Dados completos processados do webhook
    corpo_bruto = models.TextField(blank=True, null=True)  # Corpo bruto da requisição
    recebido_em = models.DateTimeField(auto_now_add=True)  # Data/hora do recebimento

    def __str__(self):
        return f"{self.tipo} - {self.recebido_em}"
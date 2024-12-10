import json
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from django.urls import get_resolver
from mercadopago import SDK
import mercadopago

from pagamentos.models import WebhookLog
from django.views.decorators.csrf import csrf_exempt
from .models import WebhookLog

from registro.models import Produto, Pedido, Vendedor
from registro.models import Usuario  # Ajuste conforme necessário

from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
def mercadopago_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))

            if data.get("type") == "payment":
                payment_id = data.get("data", {}).get("id")

                sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
                payment_info = sdk.payment().get(payment_id)

                if payment_info["status"] == 200:
                    payment_data = payment_info["response"]
                    status = payment_data.get("status")
                    comprador_email = payment_data.get("payer", {}).get("email")
                    produto_nome = payment_data.get("description")
                    total_pago = payment_data.get("transaction_amount")

                    if status == "approved":
                        try:
                            produto = Produto.objects.get(nome=produto_nome)
                        except Produto.DoesNotExist:
                            return JsonResponse({"error": "Produto não encontrado"}, status=404)

                        try:
                            comprador = Usuario.objects.get(email=comprador_email)
                        except Usuario.DoesNotExist:
                            return JsonResponse({"error": "Comprador não encontrado no sistema"}, status=404)

                        vendedor = produto.vendedor

                        Pedido.objects.create(
                            comprador=comprador,
                            vendedor=vendedor,
                            produto=produto,
                            preco_total=total_pago,
                            status="concluido"
                        )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        return JsonResponse({"status": "success"})

    return JsonResponse({"error": "Método não permitido"}, status=405)

def listar_webhooks(request):
    webhooks = WebhookLog.objects.all().order_by('-recebido_em')  # Lista os webhooks mais recentes primeiro
    return render(request, 'pagamentos/listar_webhooks.html', {'webhooks': webhooks})
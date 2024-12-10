import base64
import json
from multiprocessing import context
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout

import mercadopago

from mercadopago import SDK
from django.conf import settings

from apps.registro.models import Avaliacao, Chat, Pagamento, Pedido, Produto, Vendedor
from apps.registro.forms import EditarPerfilForm, UsuarioCreationForm
from apps.registro.forms import ProdutoForm
from apps.registro.forms import ProdutoDisponibilidadeForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg, Count
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.mail import send_mail


from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from apps.registro.models import Produto
from apps.registro.serializers import ProdutoSerializer



class ProdutoViewSet(ViewSet):
    # Listar todos os produtos
    def list(self, request):
        produtos = Produto.objects.filter(disponibilidade=True)  # Apenas produtos disponíveis
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Obter detalhes de um produto específico
    def retrieve(self, request, pk=None):
        try:
            produto = Produto.objects.get(pk=pk)
            serializer = ProdutoSerializer(produto)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Produto.DoesNotExist:
            return Response({"error": "Produto não encontrado"}, status=status.HTTP_404_NOT_FOUND)




@login_required
def meu_perfil(request):

    """
    Exibe as informações do perfil do usuário.
    """

    return render(request, 'registration/meu_perfil.html', {'usuario': request.user})

@login_required
def editar_perfil(request):
    
    if request.method == 'POST':
        perfil_form = EditarPerfilForm(request.POST, instance=request.user)
        
        if perfil_form.is_valid():
            usuario = perfil_form.save(commit=False)
            
            # Verifica se há uma nova foto enviada como base64
            foto_base64 = request.POST.get("foto_base64")
            if foto_base64:
                usuario.foto_base64 = foto_base64  # Atualiza a foto com o valor enviado
            
            # Se o campo da foto base64 não tiver sido alterado, mantemos a foto atual
            elif not foto_base64 and request.user.foto_base64:
                usuario.foto_base64 = request.user.foto_base64

            usuario.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('meu_perfil')
    else:
        perfil_form = EditarPerfilForm(instance=request.user)

    return render(request, 'registration/editar_perfil.html', {'perfil_form': perfil_form})

@login_required
def alterar_senha(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            password_form.save()
            logout(request)  # Desloga o usuário após salvar a nova senha
            return redirect('logout_message')  # Redireciona para a página de mensagem
        else:
            messages.error(request, 'Erro ao alterar senha. Verifique os campos.')
    else:
        password_form = PasswordChangeForm(user=request.user)

    return render(request, 'registration/alterar_senha.html', {'password_form': password_form})

def pagina_inicial(request):
    """
    Redireciona para a página de login.
    """
    return redirect('/login/')

def register(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST, request.FILES)  # Inclua request.FILES para aceitar arquivos
        if form.is_valid():
            print("Arquivos recebidos:", request.FILES)  # Verifica os arquivos enviados

            user = form.save(commit=False)  # Obtenha a instância do usuário sem salvar ainda
            foto = form.cleaned_data.get('foto')  # Obtenha o arquivo da foto
            print("Foto capturada do formulário:", foto)
            if foto:
                try:
                    # Reposicione o cursor no início do arquivo antes de lê-lo
                    foto.seek(0)
                    conteudo = foto.read()
                    print("Conteúdo do arquivo (binário):", conteudo[:100])  # Exibe os primeiros 100 bytes do arquivo
                    foto_base64 = base64.b64encode(conteudo).decode('utf-8')
                    user.foto_base64 = foto_base64
                    print("Base64 gerado:", foto_base64[:100])  # Exibe os primeiros 100 caracteres do Base64
                except Exception as e:
                    print("Erro ao ler ou converter o arquivo:", str(e))  # Mostra o erro no terminal

            user.save()  # Salve o usuário no banco de dados

            # Cria o vendedor se o checkbox estiver marcado
            if user.is_vendedor:
                Vendedor.objects.create(usuario=user)

                      # Envia o e-mail de boas-vindas ao nosso sistema Distribulanche
            send_mail(
                subject='Bem-vindo ao Distribulanche!',
                message=f'Olá {user.first_name}, seu email foi registrado em nosso sistema! Obrigada por fazer parte do Distribulanche!',
                from_email='distribulanche@gmail.com',
                recipient_list=[user.email],
                fail_silently=False,
            )


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
            return redirect('marketplace')  # Redireciona para o marketplace
        else:
            return render(request, 'registration/login.html', {'error': 'Credenciais inválidas. Por favor, tente novamente.'})
    return render(request, 'registration/login.html')

# View para realizar o cadastro do produto
@login_required
def cadastrar_produto(request):
    if request.method == 'POST':
        print("Arquivos recebidos no POST:", request.FILES)  # Verifique os arquivos

        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save(commit=False)  # Obtém a instância do produto sem salvar ainda

            # Associa automaticamente o vendedor logado ao produto
            vendedor = Vendedor.objects.get(usuario=request.user)
            produto.vendedor = vendedor
            print(f"Vendedor associado: {vendedor.usuario.email}")

            foto = form.cleaned_data.get('foto')  # Obtém a foto
            if foto:
                try:
                    foto.seek(0)
                    conteudo = foto.read()
                    foto_base64 = base64.b64encode(conteudo).decode('utf-8')
                    produto.imagem_base64 = foto_base64
                    print("Base64 gerado:", foto_base64[:100])
                except Exception as e:
                    print("Erro ao ler ou converter o arquivo:", str(e))

            produto.save()  # Salva o produto no banco de dados

            print(f"Produto '{produto.nome}' salvo com sucesso!")
            return redirect('meus_produtos')  # Redireciona para a página de produtos

        else:
            print("Erros no formulário:", form.errors)

    else:
        form = ProdutoForm()

    return render(request, 'produto/cadastro_produto.html', {'form': form})


#View para exibir os produtos do vendedor
@login_required
def meus_produtos(request):
    
    vendedor = Vendedor.objects.get(usuario=request.user)  # Obtém o vendedor associado ao usuário logado
    
    if request.method == "POST":
        form = ProdutoDisponibilidadeForm(request.POST, vendedor=vendedor)
        if form.is_valid():
            form.save()  # Salva as alterações de disponibilidade
            return redirect('meus_produtos')  # Redireciona para a página de produtos após a atualização
    else:
        form = ProdutoDisponibilidadeForm(vendedor=vendedor)

    # Passando apenas os produtos do vendedor logado
    produtos = Produto.objects.filter(vendedor=vendedor)
    return render(request, 'produto/meus_produtos.html', {'form': form, 'produtos': produtos})

@login_required
def minhas_avaliacoes(request):
    avaliacoes = Avaliacao.objects.filter(avaliador=request.user)
    
    return render(request, 'produto/minhas_avaliacoes.html', {'avaliacoes': avaliacoes})


def editar_produto_view(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('meus_produtos')  # Substitua pelo nome da página inicial
    else:
        form = ProdutoForm(instance=produto)

    return render(request, 'produto/produto_editar.html', {'form': form, 'produto': produto})

def deletar_produto_view(request, id):
    print(f"Tentando deletar produto com ID: {id}")
    
    # Tenta obter o produto com base no ID
    produto = get_object_or_404(Produto, id=id)
    print(f"Produto encontrado: {produto.nome} (ID: {produto.id})")

    # Verifica se a requisição é POST
    if request.method == 'POST':
        try:
            produto.delete()
            print(f"Produto com ID {id} deletado com sucesso.")
            return redirect('meus_produtos')
        except Exception as e:
            print(f"Erro ao tentar excluir produto: {e}")
            return HttpResponse(f"Erro ao tentar excluir produto: {e}", status=500)

    # Caso o método não seja POST, retorna um erro
    print("Método HTTP inválido. Esperado: POST")
    return HttpResponse("Método HTTP inválido. Esperado: POST", status=405)

def produto_detalhes_view(request, produto_id):
    # Obter o produto pelo ID
    produto = get_object_or_404(Produto, id=produto_id, disponibilidade=True)

    # Obter avaliações do produto
    avaliacoes = Avaliacao.objects.filter(produto=produto).select_related('avaliador')
    media_avaliacoes = avaliacoes.aggregate(avg_rating=Avg('nota'))['avg_rating'] or 0
    total_avaliacoes = avaliacoes.count()

    # Contexto para o template
    context = {
        'produto': produto,
        'avaliacoes': avaliacoes,
        'media_avaliacoes': media_avaliacoes,
        'total_avaliacoes': total_avaliacoes,
    }

    return render(request, 'produto/produto_detalhes.html', context)


def produto_comprar_view(request, produto_id):
    # Obter o produto pelo ID
    produto = get_object_or_404(Produto, id=produto_id, disponibilidade=True)

    # Capturar a quantidade enviada pelo formulário (ou usar 1 como padrão)
    quantidade = int(request.POST.get("quantidade", 1))
    total_preco = float(produto.preco) * quantidade

    try:
        import mercadopago
    except ImportError as e:
        print("Erro ao importar o pacote Mercado Pago:", e)
        return HttpResponse("Erro ao importar o pacote Mercado Pago. Certifique-se de que o pacote está instalado.", status=500)

    # Configurar o Mercado Pago
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    preference_data = {
        "items": [
            {
                "title": produto.nome,
                "quantity": 1,  #quantidade fixa para que o MP não altere o nome do produto
                "unit_price": total_preco,  # Total calculado
            }
        ],
        "back_urls": { # Redirecionamento automático para cada caso
            "success": "https://seusite.com/sucesso",
            "failure": "https://seusite.com/erro",
            "pending": "https://seusite.com/pendente",
        },
        "auto_return": "approved",  # Redirecionamento automático para "success"
        "notification_url": "https://0564-189-126-44-164.ngrok-free.app/pagamentos/webhook/",  # URL para receber notificações
    }

    # Criar a preferência de pagamento
    try:
        preference_response = sdk.preference().create(preference_data)
        link_pagamento = preference_response["response"]["init_point"]
        return JsonResponse({"link_pagamento": link_pagamento})  # Retorna o link como JSON
    except Exception as e:
        return JsonResponse({"error": "Erro ao gerar link de pagamento."}, status=500)




    
@csrf_exempt
def pagamento_notificacao(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id_transacao = data.get("data", {}).get("id")

        # Processar o status do pagamento
        if id_transacao:
            sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
            payment_info = sdk.payment().get(id_transacao)

            status = payment_info["response"]["status"]
            pedido_id = payment_info["response"]["external_reference"]

            # Atualizar o status do pagamento
            pedido = Pedido.objects.get(id=pedido_id)
            pagamento, created = Pagamento.objects.get_or_create(
                id_transacao=id_transacao,
                pedido=pedido
            )
            pagamento.status = status
            pagamento.save()

    return JsonResponse({"message": "Notificação recebida com sucesso"})


@login_required
def chat(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    if request.method == "POST":
        mensagem = request.POST.get('mensagem')
        vendedor = produto.vendedor

        # Criar a mensagem no banco de dados
        nova_mensagem = Chat.objects.create(
            comprador=request.user,
            vendedor=vendedor,
            produto=produto,
            mensagem=mensagem
        )

        return JsonResponse({
            'status': 'sucesso',
            'dados': {
                'mensagem': nova_mensagem.mensagem,
                'data_horario': nova_mensagem.data_horario.strftime('%d/%m/%Y %H:%M:%S'),
                'usuario': request.user.email,
            }
        })

    elif request.method == "GET":
        # Recuperar todas as mensagens relacionadas ao produto
        mensagens = Chat.objects.filter(produto=produto).order_by('data_horario')

        mensagens_serializadas = [
            {
                'usuario': chat.comprador.email if chat.comprador == request.user else chat.vendedor.email,
                'mensagem': chat.mensagem,
                'data_horario': chat.data_horario.strftime('%d/%m/%Y %H:%M:%S'),
            }
            for chat in mensagens
        ]
        return JsonResponse({'mensagens': mensagens_serializadas})
@login_required
def obter_mensagens(request, produto_id):
    if request.method == "GET":
        # Último ID para otimizar a busca
        ultimo_id = int(request.GET.get("ultimo_id", 0))
        mensagens = Chat.objects.filter(produto_id=produto_id, id__gt=ultimo_id).order_by('data_horario')

        mensagens_json = []
        for mensagem in mensagens:
            if mensagem.comprador == request.user:
                nome = "Você"  # O cliente vê "Você" para suas próprias mensagens
            elif mensagem.vendedor == request.user:
                nome = "Você"  # O vendedor vê "Você" para suas próprias mensagens
            else:
                # Caso contrário, exibe o nome do outro participante
                nome = mensagem.comprador.first_name if mensagem.vendedor.usuario == request.user else "Vendedor"

            mensagens_json.append({
                "id": mensagem.id,
                "mensagem": mensagem.mensagem,
                "nome": nome,
                "data_horario": mensagem.data_horario.strftime("%d/%m/%Y %H:%M"),
                "is_comprador": mensagem.comprador == request.user
            })

        return JsonResponse({"mensagens": mensagens_json}, status=200)
    return JsonResponse({"erro": "Método inválido"}, status=400)

import base64
from multiprocessing import context
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from apps.registro.models import Avaliacao, Produto, Vendedor
from .forms import UsuarioCreationForm
from .forms import ProdutoForm
from .forms import ProdutoDisponibilidadeForm
from django.contrib.auth.decorators import login_required
from apps.registro.models import Vendedor



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

            # Autentica e loga o usuário
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('marketplace/lanches.html')
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

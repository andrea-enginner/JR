import base64
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Vendedor
from .forms import UsuarioCreationForm


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
                return redirect('/marketplace/lanches/')
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
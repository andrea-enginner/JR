from django.db.models import Q, Avg, Count
from django.shortcuts import render
from registro.models import Produto
from django.db.models import Avg, Count, Q, Func, F



def marketplace_view(request):
    # Termo de pesquisa
    search_query = request.GET.get('search', '')

    # Filtros de ordenação
    sort_by = request.GET.get('sort', 'nome')  # Padrão: ordenação por nome

    # Query base: apenas produtos disponíveis
    produtos = Produto.objects.filter(disponibilidade=True).annotate(
        avg_rating=Avg('avaliacoes__nota'),
        num_avaliacoes=Count('avaliacoes')
    )

    # Aplicar pesquisa (filtro por nome ou descrição)
    if search_query:
        produtos = produtos.filter(
            Q(nome__icontains=search_query) | Q(descricao__icontains=search_query)
        )

    # Aplicar ordenação
    if sort_by == 'mais_vendidos':
        produtos = produtos.order_by('-num_vendas')
    elif sort_by == 'mais_avaliados':
        produtos = produtos.order_by('-num_avaliacoes')
    elif sort_by == 'menor_preco':
        produtos = produtos.order_by('preco')
    elif sort_by == 'maior_preco':
        produtos = produtos.order_by('-preco')
    elif sort_by == 'nome':  # Ordenar por nome (ignorar maiúsculas)
        produtos = produtos.annotate(lower_nome=Func(F('nome'), function='LOWER')).order_by('lower_nome')

    return render(request, 'marketplace/home.html', {'produtos': produtos})
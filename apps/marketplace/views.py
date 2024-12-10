from django.db.models import Q, Avg, Count, Func, F
from django.core.paginator import Paginator
from django.shortcuts import render
from apps.registro.models import Produto

def marketplace_view(request):
    # Termo de pesquisa
    search_query = request.GET.get('search', '')

    # Filtros de ordenação
    sort_by = request.GET.get('sort', 'nome')  # Padrão: ordenação por nome

    # Query base: apenas produtos disponíveis
    produtos = Produto.objects.filter(disponibilidade=True, num_produtos__gte=1).annotate(
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

    # Paginação
    paginator = Paginator(produtos, 9)  # Exibir 9 produtos por página
    page_number = request.GET.get('page')  # Obter número da página atual
    page_obj = paginator.get_page(page_number)

    return render(request, 'marketplace/home.html', {'page_obj': page_obj, 'search_query': search_query, 'sort_by': sort_by})

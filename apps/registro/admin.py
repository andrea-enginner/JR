from django.contrib import admin
from .models import Usuario, Vendedor, Produto, Pedido, Avaliacao, Chat, Notificacao, Pagamento

# Inline para Produtos dentro da página do Vendedor
class ProdutoInline(admin.TabularInline):
    model = Produto
    extra = 1

# Inline para Pedidos relacionados ao Vendedor
class PedidoVendedorInline(admin.TabularInline):
    model = Pedido
    fk_name = "vendedor"  # Especifica que o inline é filtrado pelo campo 'vendedor'
    extra = 1

# Inline para Pedidos relacionados ao Comprador (Usuario)
class PedidoCompradorInline(admin.TabularInline):
    model = Pedido
    fk_name = "comprador"  # Especifica que o inline é filtrado pelo campo 'comprador'
    extra = 1

# Inline para Avaliações relacionadas ao Produto
class AvaliacaoInline(admin.TabularInline):
    model = Avaliacao
    extra = 1

# Inline para Chat entre Vendedor e Comprador
class ChatVendedorInline(admin.TabularInline):
    model = Chat
    fk_name = "vendedor"
    extra = 1

class ChatCompradorInline(admin.TabularInline):
    model = Chat
    fk_name = "comprador"
    extra = 1

# Inline para Notificações de um Usuário
class NotificacaoInline(admin.TabularInline):
    model = Notificacao
    extra = 1

# Inline para Pagamentos associados a Pedidos
class PagamentoInline(admin.TabularInline):
    model = Pagamento
    extra = 1

# Configuração do Admin para o Vendedor
class VendedorAdmin(admin.ModelAdmin):
    inlines = [ProdutoInline, PedidoVendedorInline, ChatVendedorInline]
    list_display = ('usuario', 'telefone', 'localizacao', 'status')
    search_fields = ('usuario__email', 'localizacao', 'telefone')
    list_filter = ('status',)

# Configuração do Admin para o Produto, com avaliações
class ProdutoAdmin(admin.ModelAdmin):
    inlines = [AvaliacaoInline]
    list_display = ('nome', 'vendedor', 'preco', 'disponibilidade', 'num_vendas')
    search_fields = ('nome', 'descricao', 'vendedor__usuario__email')
    list_filter = ('disponibilidade',)

# Configuração do Admin para o Usuario, com pedidos, notificações e chats
class UsuarioAdmin(admin.ModelAdmin):
    inlines = [PedidoCompradorInline, NotificacaoInline, ChatCompradorInline]
    list_display = ('email', 'telefone', 'is_vendedor', 'is_staff', 'is_active')
    search_fields = ('email', 'telefone')
    list_filter = ('is_vendedor', 'is_staff', 'is_active')

# Configuração do Admin para o Pedido
class PedidoAdmin(admin.ModelAdmin):
    inlines = [PagamentoInline]
    list_display = ('id', 'comprador', 'vendedor', 'produto', 'preco_total', 'status', 'atualizado_em')
    search_fields = ('comprador__email', 'vendedor__usuario__email', 'produto__nome')
    list_filter = ('status', 'atualizado_em')

# Registro dos modelos no admin
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Vendedor, VendedorAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Avaliacao)
admin.site.register(Chat)
admin.site.register(Notificacao)
admin.site.register(Pagamento)

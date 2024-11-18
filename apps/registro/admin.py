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

# Inline para Pagamentos associados a Produtos
class PagamentoInline(admin.TabularInline):
    model = Pagamento
    extra = 1

# Configuração do Admin para o Vendedor
class VendedorAdmin(admin.ModelAdmin):
    inlines = [ProdutoInline, PedidoVendedorInline, ChatVendedorInline]

# Configuração do Admin para o Produto, com avaliações e pagamentos
class ProdutoAdmin(admin.ModelAdmin):
    inlines = [AvaliacaoInline, PagamentoInline]

# Configuração do Admin para o Usuario, com pedidos, notificações e chats
class UsuarioAdmin(admin.ModelAdmin):
    inlines = [PedidoCompradorInline, NotificacaoInline, ChatCompradorInline]

# Registro dos modelos no admin
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Vendedor, VendedorAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Pedido)
admin.site.register(Avaliacao)
admin.site.register(Chat)
admin.site.register(Notificacao)
admin.site.register(Pagamento)

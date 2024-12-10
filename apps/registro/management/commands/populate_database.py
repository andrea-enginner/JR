from django.core.management.base import BaseCommand
from faker import Faker
from random import randint, choice, uniform
from decimal import Decimal
from registro.models import Usuario, Vendedor, Produto, Pedido, Avaliacao, Chat, Notificacao, Pagamento


class Command(BaseCommand):
    help = 'Popula o banco de dados com dados fictícios'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Cria usuários
        usuarios = []
        for _ in range(50):
            usuario = Usuario.objects.create_user(
                email=fake.email(),
                password="senha123",
                telefone=fake.phone_number(),
                is_vendedor=fake.boolean(),
                foto_base64=fake.image_url(),
            )
            usuarios.append(usuario)

        # Cria vendedores
        vendedores = []
        for usuario in filter(lambda u: u.is_vendedor, usuarios):
            vendedor = Vendedor.objects.create(
                usuario=usuario,
                localizacao=fake.address(),
                telefone=fake.phone_number(),
                status=fake.boolean(),
            )
            vendedores.append(vendedor)

        # Cria produtos
        produtos = []
        for _ in range(50):
            vendedor = choice(vendedores)
            produto = Produto.objects.create(
                vendedor=vendedor,
                nome=fake.word().capitalize(),
                descricao=fake.text(),
                preco=Decimal(round(uniform(0.10, 100), 2)),
                disponibilidade=fake.boolean(),
                num_vendas=randint(0, 100),
                num_produtos=randint(1, 50),
                imagem_base64=fake.image_url(),
            )
            produtos.append(produto)

        # Cria pedidos
        pedidos = []
        for _ in range(50):
            comprador = choice(usuarios)
            produto = choice(produtos)
            vendedor = produto.vendedor
            pedido = Pedido.objects.create(
                comprador=comprador,
                vendedor=vendedor,
                produto=produto,
                preco_total=produto.preco * randint(1, 5),
                status=choice(["pendente", "concluido"]),
            )
            pedidos.append(pedido)

        # Cria avaliações
        for _ in range(50):
            produto = choice(produtos)
            avaliador = choice(usuarios)
            Avaliacao.objects.get_or_create(
                produto=produto,
                avaliador=avaliador,
                defaults={
                    "nota": randint(1, 5),
                    "comentario": fake.text(),
                }
            )

        # Cria chats
        for _ in range(50):
            comprador = choice(usuarios)
            produto = choice(produtos)
            vendedor = produto.vendedor
            Chat.objects.create(
                comprador=comprador,
                vendedor=vendedor,
                produto=produto,
                mensagem=fake.text(),
            )

        # Cria notificações
        for _ in range(50):
            usuario = choice(usuarios)
            Notificacao.objects.create(
                usuario=usuario,
                mensagem=fake.text(),
            )

        # Cria pagamentos
        for pedido in pedidos:
            Pagamento.objects.create(
                pedido=pedido,
                status=choice(["pendente", "aprovado", "recusado"]),
                metodo="Mercado Pago",
                id_transacao=fake.uuid4(),
            )

        self.stdout.write(self.style.SUCCESS("Dados fictícios criados com sucesso!"))

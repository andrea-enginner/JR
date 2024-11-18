from django.core.management.base import BaseCommand
from faker import Faker
from apps.registro.models import Usuario, Vendedor, Produto, Pedido, Avaliacao, Chat, Notificacao, Pagamento
import random

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados fictícios'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Função para gerar telefone com no máximo 15 caracteres
        def generate_phone():
            return fake.phone_number()[:15]

        # Criar usuários (200 usuários no total)
        usuarios = []
        for _ in range(200):
            usuario = Usuario.objects.create(
                nome=fake.name(),
                email=fake.unique.email(),
                telefone=generate_phone(),
                is_vendedor=fake.boolean()
            )
            usuarios.append(usuario)
        
        # Criar vendedores (pelo menos 100 vendedores)
        vendedores = []
        for usuario in usuarios[:100]:  # Converte os primeiros 100 usuários em vendedores
            vendedor = Vendedor.objects.create(
                usuario=usuario,
                localizacao=fake.address(),
                telefone=generate_phone(),
                status=fake.boolean()
            )
            vendedores.append(vendedor)
        
        # Criar produtos (500 produtos no total)
        produtos = []
        for vendedor in vendedores:
            for _ in range(5):  # 5 produtos por vendedor
                produto = Produto.objects.create(
                    vendedor=vendedor,
                    nome=fake.word().capitalize(),
                    descricao=fake.text(),
                    preco=round(random.uniform(10.0, 100.0), 2),
                    disponibilidade=fake.boolean()
                )
                produtos.append(produto)

        # Criar pedidos (200 pedidos no total)
        pedidos = []
        for _ in range(200):
            comprador = random.choice([u for u in usuarios if not u.is_vendedor])
            vendedor = random.choice(vendedores)
            produto = random.choice(produtos)
            pedido = Pedido.objects.create(
                comprador=comprador,
                vendedor=vendedor,
                produto=produto,
                preco_total=produto.preco,
                status=random.choice(['pendente', 'concluido'])
            )
            pedidos.append(pedido)
        
        # Criar avaliações (200 avaliações no total)
        for _ in range(200):
            avaliador = random.choice([u for u in usuarios if not u.is_vendedor])
            produto = random.choice(produtos)
            Avaliacao.objects.create(
                produto=produto,
                avaliador=avaliador,
                nota=random.randint(1, 5),
                comentario=fake.text()
            )

        # Criar chats (200 mensagens de chat no total)
        for _ in range(200):
            vendedor = random.choice(vendedores)
            comprador = random.choice([u for u in usuarios if not u.is_vendedor])
            Chat.objects.create(
                vendedor=vendedor,
                comprador=comprador,
                mensagem=fake.sentence(),
                data_horario=fake.date_time_this_year()
            )

        # Criar notificações (200 notificações no total)
        for _ in range(200):
            usuario = random.choice(usuarios)
            Notificacao.objects.create(
                usuario=usuario,
                mensagem=fake.sentence(),
                enviado_em=fake.date_time_this_year()
            )

        # Criar pagamentos (200 pagamentos no total)
        for _ in range(200):
            produto = random.choice(produtos)
            Pagamento.objects.create(
                produto=produto,
                tipo_pagamento=random.choice(['cartao', 'boleto']),
                pago_em=fake.date_time_this_year()
            )

        self.stdout.write(self.style.SUCCESS('Banco de dados populado com centenas de registros em cada tabela!'))

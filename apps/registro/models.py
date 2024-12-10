from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import EmailValidator
from django.core.validators import RegexValidator


# Gerenciador para criar usuários personalizados
class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Regex para validar números de telefone no formato (XX) XXXX-XXXX ou (XX) XXXXX-XXXX
telefone_validator = RegexValidator(
    regex=r'^\(\d{2}\) \d{4,5}-\d{4}$',
    message="O número de telefone deve estar no formato (XX) XXXX-XXXX ou (XX) XXXXX-XXXX."
)

# Modelo do usuário personalizado
class Usuario(AbstractUser):
    email = models.EmailField(validators=[EmailValidator()] ,unique=True)
    telefone = models.CharField(
        max_length=15, 
        validators=[telefone_validator],
        blank=True, 
        null=True
    )
    is_vendedor = models.BooleanField(default=False)
    foto_base64 = models.TextField(blank=True, null=True)
    # Campos não usados pelo AbstractUser
    username = None

    # Campo único para autenticação
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UsuarioManager()

    def __str__(self):
        return self.email


class Vendedor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='vendedor')
    localizacao = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.usuario.email


from django.db import models

class Produto(models.Model):
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name='produtos')
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2, validators=[
        MinValueValidator(0.10),  # O preço não pode ser menor ou igual a 0.10
        MaxValueValidator(100)   # O preço máximo será 100
    ])
    disponibilidade = models.BooleanField(default=True)
    num_vendas = models.PositiveIntegerField(default=0)  
    num_produtos = models.IntegerField(validators=[MinValueValidator(0)])

    imagem_base64 = models.TextField(blank=True, null=True)  # Armazena a versão Base64 da imagem

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    comprador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pedidos')
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name='pedidos')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco_total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('pendente', 'Pendente'), ('concluido', 'Concluído')])
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.comprador.email} para {self.vendedor.usuario.email}"

class Avaliacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='avaliacoes')
    avaliador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.PositiveIntegerField()
    comentario = models.TextField(blank=True, null=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('produto', 'avaliador')  # Garante que um usuário avalie apenas uma vez um produto

    def __str__(self):
        return f"Avaliação de {self.avaliador.email} no produto {self.produto.nome}"


class Chat(models.Model):
    comprador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="comprador_chats")
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE, related_name="vendedor_chats")  # Altere para Vendedor
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="chats")
    mensagem = models.TextField()
    data_horario = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        
        return f"Chat: {self.comprador} -> {self.vendedor} ({self.produto.nome})"


class Notificacao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notificacoes')
    mensagem = models.TextField()
    enviado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificação para {self.usuario.email}"


class Pagamento(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="pagamentos")
    status = models.CharField(max_length=50, choices=[("pendente", "Pendente"), ("aprovado", "Aprovado"), ("recusado", "Recusado")])
    metodo = models.CharField(max_length=50, default="Mercado Pago")
    id_transacao = models.CharField(max_length=100, unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pagamento {self.id_transacao} - {self.status}"
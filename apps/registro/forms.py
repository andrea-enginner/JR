from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario
from .models import Produto
import base64

class UsuarioCreationForm(UserCreationForm):
    foto = forms.ImageField(required=False, label="Foto de Perfil")  # Campo de upload de imagem

    class Meta:
        model = Usuario
        fields = ('email', 'first_name', 'last_name', 'telefone', 'is_vendedor', 'foto')


    def save(self, commit=True):
        user = super().save(commit=False)  # Obtém a instância do usuário sem salvar ainda
        foto = self.cleaned_data.get('foto')  # Obtém o arquivo de imagem enviado pelo usuário
        if foto:
            # Converte a imagem para Base64
            user.foto_base64 = base64.b64encode(foto.read()).decode('utf-8')
        if commit:
            user.save()
        return user


class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('email', 'telefone', 'is_vendedor')


class ProdutoForm(forms.ModelForm):
    foto = forms.ImageField(required=False, label="Imagem do produto")  # Campo de upload de imagem

    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'disponibilidade', 'foto']  # Incluindo 'foto'

    def save(self, commit=True):
        produto = super().save(commit=False)  # Obtém a instância do produto sem salvar ainda
        foto = self.cleaned_data.get('foto')  # Obtém o arquivo de imagem enviado pelo usuário
        if foto:
            # Converte a imagem para Base64
            foto_base64 = base64.b64encode(foto.read()).decode('utf-8')
            produto.imagem_base64 = foto_base64  # Salva o Base64 no campo imagem_base64
        if commit:
            produto.save()  # Salva o produto no banco de dados
        return produto


class ProdutoDisponibilidadeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.vendedor = kwargs.pop('vendedor', None)
        super().__init__(*args, **kwargs)

        produtos = Produto.objects.filter(vendedor=self.vendedor)
        for produto in produtos:
            self.fields[f'produto_{produto.id}'] = forms.BooleanField(
                required=False,  # Permite valores False
                initial=produto.disponibilidade,
                label=produto.nome,
                widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
            )

    def save(self):
        for produto in Produto.objects.filter(vendedor=self.vendedor):
            disponibilidade = self.cleaned_data.get(f'produto_{produto.id}', False)  # Default é False
            produto.disponibilidade = disponibilidade  # Já é um valor booleano
            produto.save()

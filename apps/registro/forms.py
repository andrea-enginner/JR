from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario
from .models import Produto
import base64

class UsuarioCreationForm(UserCreationForm):
    foto = forms.ImageField(required=False, label="Foto de Perfil")  # Campo de upload de imagem
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite uma senha forte',
        }),
    )
    password2 = forms.CharField(
        label="Confirme sua senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repita a senha',
        }),
    )

    class Meta:
        model = Usuario
        fields = ('email', 'first_name', 'last_name', 'telefone', 'is_vendedor', 'foto', 'password1', 'password2')

        labels = {
            'email': 'Endereço de Email',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'telefone': 'Número de Telefone',
            'is_vendedor': 'Deseja ser vendedor?',
            'foto': 'Foto de Perfil',
            'password1': 'Senha',
            'password2': 'Confirme sua senha',
        }

            # Personalizando widgets (opcional)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu sobrenome'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) XXXXX-XXXX'}),
            'is_vendedor': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }

        


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


        
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email']

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'foto_base64']
        widgets = {
            'foto_base64': forms.HiddenInput(),  # Campo oculto para armazenar base64
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se o usuário já tiver uma foto, preenche o campo foto_base64 com a foto atual
        if self.instance and self.instance.foto_base64:
            self.fields['foto_base64'].initial = self.instance.foto_base64



class ProdutoForm(forms.ModelForm):
    foto = forms.ImageField(required=False, label="Imagem do produto")  # Campo de upload de imagem

    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'disponibilidade', 'foto', 'num_produtos']  # Incluindo 'foto' e 'num_produtos'

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

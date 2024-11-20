from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario
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

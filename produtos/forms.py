from django import forms
from produtos.models import Produto
from django.contrib.auth.models import User
from .models import Produtor

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'tipo', 'preco', 'unidade_medida']


# produtos/forms.py

from django import forms
from .models import Produtor

class ProdutorForm(forms.ModelForm):
    class Meta:
        model = Produtor
        fields = ['user', 'nome', 'email', 'telefone']


    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['nome'],  # Usando o nome como username
            password=self.cleaned_data['senha'],
            email=self.cleaned_data['email']
        )
        produtor = super().save(commit=False)
        produtor.user = user
        if commit:
            produtor.save()
        return produtor

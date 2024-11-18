import self

from produtos.models import Produto
from django import forms
from .models import Produtor
from django.contrib.auth.hashers import make_password
from .models import Estoque

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'tipo', 'preco','quantidade']

        def clean(self):
            cleaned_data = super().clean()
            nome = cleaned_data.get("nome")
            tipo = cleaned_data.get("tipo")

            if Produto.objects.filter(nome=nome, tipo=tipo).exists():
                raise forms.ValidationError("Este produto já existe no sistema.")

            return cleaned_data


# produtos/forms.py



class ProdutorForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput, required=False)  # Senha opcional, mas com asteriscos

    class Meta:
        model = Produtor
        fields = ['usuario', 'senha', 'nome', 'email', 'telefone', 'cpf']

    def clean_senha(self):
        senha = self.cleaned_data.get('senha')
        if senha:
            return make_password(senha)  # Se a senha for fornecida, faz o hash dela
        return None

    class EstoqueForm(forms.ModelForm):
        class Meta:
            model = Estoque
            fields = ['quantidade']  # ou outros campos que você queira manipular

        def clean_quantidade(self):
            quantidade = self.cleaned_data.get('quantidade')
            if quantidade <= 0:
                raise forms.ValidationError("A quantidade deve ser maior que zero.")
            return quantidade

class ProdutorPerfilForm(forms.ModelForm):
    class Meta:
        model = Produtor
        fields = ['nome', 'email', 'telefone', 'cpf']  # Não inclui 'usuario' e 'senha'

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if not cpf:
            return ''
        # Lógica de validação do CPF (se necessário)
        return cpf
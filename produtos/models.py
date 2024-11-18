from django.db import models
from django.contrib.auth.models import User

# Modelo para a página inicial
class PaginaInicial(models.Model):
    titulo = models.CharField(max_length=200, default="Bem-vindo à Cervejaria")
    imagem_fundo = models.ImageField(upload_to='imagens/', blank=True, null=True)  # Campo para imagem de fundo
    link_login_gerente = models.CharField(max_length=200, default="/login/gerente/")
    link_login_produtor = models.CharField(max_length=200, default="/login/produtor/")
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

# Modelo para Produtos
class Produto(models.Model):
    TIPO_PRODUTO_CHOICES = [
        ('malte', 'Malte'),
        ('lupulo', 'Lúpulo'),
        ('levedura', 'Levedura'),
        ('agua', 'Água'),
        ('produto_final', 'Produto Final'),
    ]

    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_PRODUTO_CHOICES)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField(default=0)  # Quantidade disponível no estoque
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('nome', 'tipo')

    def __str__(self):
        return self.nome

class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)  # Relacionamento com o modelo Produto
    quantidade = models.IntegerField(default=0)
    valor_total = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade} em estoque"







# Modelo para Logs do Sistema
class LogSistema(models.Model):
    acao = models.CharField(max_length=255)
    usuario = models.CharField(max_length=100)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.acao} por {self.usuario} em {self.data}"

# Modelo para Produtores
from django.db import models
from django.contrib.auth.hashers import make_password  # Para hash da senha

class Produtor(models.Model):
    usuario = models.CharField(max_length=150, unique=True)  # Nome do usuário
    senha = models.CharField(max_length=255)  # Senha do produtor
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    telefone = models.CharField(max_length=15)
    cpf = models.CharField(max_length=15, null=True, blank=True)  # Opcional
    created_at = models.DateTimeField(auto_now_add=True)  # Data de criação

    class Meta:
        db_table = 'produtor'  # Define explicitamente o nome da tabela como 'produtor'

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if self.senha:  # Apenas faz o hash se a senha for fornecida
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)



class ConteudoLogin(models.Model):
    tipo_login = models.CharField(max_length=50)
    titulo = models.CharField(max_length=100)
    imagem_fundo = models.ImageField(upload_to='imagens/', blank=True, null=True)

    def __str__(self):
        return self.titulo


from django.db import models
from django.contrib.auth.models import User
from produtos.models import Produto


class EstoqueChange(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)
    tipo_alteracao = models.CharField(max_length=20, choices=[('adicao', 'Adição'), ('venda', 'Venda')])
    produtor = models.ForeignKey(User, on_delete=models.CASCADE)  # Associar ao produtor logado

    def __str__(self):
        return f'{self.produto.nome} - {self.tipo_alteracao} - {self.quantidade}'

class RelatorioEstoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    produtor = models.ForeignKey(User, on_delete=models.CASCADE)  # Usando o User ou seu modelo de Produtor
    quantidade_alterada = models.IntegerField()
    tipo_alteracao = models.CharField(
        max_length=20,
        choices=[('adicao', 'Adição'), ('venda', 'Venda')]
    )
    data_alteracao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.produto.nome} - {self.tipo_alteracao} - {self.quantidade_alterada}'
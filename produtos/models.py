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




# Modelo para Produtores
from django.db import models


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
        return self.usuario


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
    tipo_alteracao = models.CharField(max_length=50)  # Tipo de alteração: 'Entrada' ou 'Remoção'
    produtor = models.ForeignKey(Produtor, on_delete=models.CASCADE)  # Associar ao produtor logado

    def __str__(self):
        return f'{self.produto.nome} - {self.tipo_alteracao} - {self.quantidade}'

class RelatorioEstoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    produtor = models.ForeignKey(Produtor, on_delete=models.SET_NULL, null=True, blank=True)  # Torna opcional
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Para gerentes
    quantidade_alterada = models.IntegerField()
    tipo_alteracao = models.CharField(max_length=50)
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'RelatorioEstoque'

    def __str__(self):
        return f"{self.produto.nome} - {self.tipo_alteracao} por {self.produtor or self.admin.username}"



class Pedido(models.Model):
    produtor = models.ForeignKey(Produtor, on_delete=models.SET_NULL, null=True, blank=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - Produtor/Admin: {self.produtor or self.admin}"



class LogSistema(models.Model):
    produtor = models.ForeignKey(Produtor, on_delete=models.CASCADE)
    acao = models.CharField(max_length=255)
    data_entrada = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'LogSistema'

    def __str__(self):
        return f"{self.produtor.usuario} - {self.acao}"
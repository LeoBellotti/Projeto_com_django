from django.db import models
from django.contrib.auth.models import User


# Model para Produtos
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
    unidade_medida = models.CharField(max_length=20)  # Exemplo: kg, litros
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


# Model para Estoque
class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade} em estoque"


# Model para Pedidos
class Pedido(models.Model):
    STATUS_PEDIDO_CHOICES = [
        ('em_processamento', 'Em Processamento'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]

    cliente_nome = models.CharField(max_length=100)
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_PEDIDO_CHOICES, default='em_processamento')

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente_nome}"


# Model para Itens de Pedido
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade} unidades"


# Model para Receitas
class Receita(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


# Model para Itens de Receita
class ItemReceita(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.receita.nome} - {self.produto.nome}"


# Model para Logs do Sistema
class LogSistema(models.Model):
    acao = models.CharField(max_length=255)
    usuario = models.CharField(max_length=100)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.acao} por {self.usuario} em {self.data}"



# produtos/models.py

class Produtor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return self.nome

class PaginaInicial(models.Model):
    titulo = models.CharField(max_length=200, default="Bem-vindo à Cervejaria")
    imagem_fundo = models.ImageField(upload_to='imagens/', blank=True, null=True)  # Campo para a imagem de fundo
    link_login_gerente = models.URLField(max_length=200, default="/login/gerente/")
    link_login_produtor = models.URLField(max_length=200, default="/login/produtor/")
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

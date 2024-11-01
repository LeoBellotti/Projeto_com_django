
from produtos.models import Produto, PaginaInicial
from produtos.forms import ProdutoForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProdutorForm
from .models import Produtor


# View para listar produtos
def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'produtos/lista_Produtos.html', {'produtos': produtos})

# View para adicionar um novo produto
def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/adicionar_Produto.html', {'form': form})

# View para editar um produto
def editar_produto(request, pk):
    produto = Produto.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/editar_Produto.html', {'form': form})

# View para deletar um produto
def deletar_produto(request, pk):
    produto = Produto.objects.get(pk=pk)
    if request.method == 'POST':
        produto.delete()
        return redirect('lista_produtos')
    return render(request, 'produtos/deletar_Produto.html', {'produto': produto})

# produtos/views.py

def login_gerente(request):
    return render(request, 'produtos/login_gerente.html')  # Template do login do gerente

def login_produtor(request):
    return render(request, 'produtos/login_produtor.html')  # Template do login do vendedor/produtor
# produtos/views.py


from django.shortcuts import render

def exibir_pagina_inicial(request):
    conteudo = PaginaInicial.objects.last()  # Pega o conteúdo mais recente
    return render(request, 'produtos/pagina_inicial.html', {'conteudo': conteudo})

def listar_produtores(request):
    produtores = Produtor.objects.all()
    return render(request, 'produtos/listar_produtores.html', {'produtores': produtores})

def cadastrar_produtor(request):
    if request.method == 'POST':
        form = ProdutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_produtores')
    else:
        form = ProdutorForm()
    return render(request, 'produtos/cadastrar_produtor.html', {'form': form})
def editar_produtor(request, pk):
    produtor = get_object_or_404(Produtor, pk=pk)
    if request.method == 'POST':
        form = ProdutorForm(request.POST, instance=produtor)
        if form.is_valid():
            form.save()
            return redirect('listar_produtores')
    else:
        form = ProdutorForm(instance=produtor)
    return render(request, 'produtos/editar_produtor.html', {'form': form})

def deletar_produtor(request, pk):
    produtor = get_object_or_404(Produtor, pk=pk)
    if request.method == 'POST':
        produtor.delete()
        return redirect('listar_produtores')
    return render(request, 'produtos/deletar_produtor.html', {'produtor': produtor})


def gerenciar_produtores(request):
    if request.method == 'POST':
        form = ProdutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_produtores')  # Redireciona após salvar
    else:
        form = ProdutorForm()

    produtores = Produtor.objects.all()  # Lista todos os produtores
    return render(request, 'produtos/gerenciar_produtores.html', {'form': form, 'produtores': produtores})

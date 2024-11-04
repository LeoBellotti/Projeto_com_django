
from .models import Produto, PaginaInicial, ConteudoLogin
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto
from .forms import ProdutoForm

@login_required(login_url='login_gerente')  # Especifica o redirecionamento para a página de login
def menu_gerente(request, action=None, pk=None):
    produtos = Produto.objects.all()

    if action == 'gerenciar':
        return render(request, 'produtos/menu_gerente.html', {
            'produtos': produtos,
            'action': 'gerenciar',

        })

    elif action == 'add':
        form = ProdutoForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            form.save()
            messages.success(request, 'Produto adicionado com sucesso.')
            return redirect('menu_gerente_action', action='gerenciar')
        return render(request, 'produtos/menu_gerente.html', {
            'form': form,
            'action': 'add',

        })

    elif action == 'edit' and pk:
        produto = get_object_or_404(Produto, pk=pk)
        form = ProdutoForm(request.POST or None, instance=produto)
        if request.method == 'POST' and form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso.')
            return redirect('menu_gerente_action', action='gerenciar')
        return render(request, 'produtos/menu_gerente.html', {
            'form': form,
            'produto': produto,
            'action': 'edit',

        })

    elif action == 'delete' and pk:
        produto = get_object_or_404(Produto, pk=pk)
        if request.method == 'POST':
            produto.delete()
            messages.success(request, 'Produto excluído com sucesso.')
            return redirect('menu_gerente_action', action='gerenciar')
        return render(request, 'produtos/menu_gerente.html', {
            'produto': produto,
            'action': 'delete',

        })

    return render(request, 'produtos/menu_gerente.html', {
        'produtos': produtos,
        'action': action if action else 'inicio',

    })

def login_gerente(request):
    conteudo = get_object_or_404(ConteudoLogin, tipo_login='gerente')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu_gerente')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')

    return render(request, 'produtos/login_gerente.html', {'conteudo': conteudo})


def exibir_pagina_inicial(request):
    conteudo = PaginaInicial.objects.last()
    return render(request, 'produtos/pagina_inicial.html', {'conteudo': conteudo})


def login_produtor(request):
    conteudo = get_object_or_404(ConteudoLogin, tipo_login='produtor')
    return render(request, 'produtos/login_produtor.html', {'conteudo': conteudo})

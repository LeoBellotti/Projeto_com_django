from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import Produto, PaginaInicial, ConteudoLogin, EstoqueChange
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto
from .models import Produtor,Estoque
from .forms import ProdutoForm, ProdutorPerfilForm
from .forms import ProdutorForm
from django.urls import reverse


@login_required(login_url='login_gerente')  # Especifica o redirecionamento para a página de login

def menu_gerente(request, action=None, pk=None):
    if action == 'listar_produtores':
        produtores = Produtor.objects.all()  # Removido qualquer filtro desnecessário
        return render(request, 'produtos/menu_gerente.html', {'produtores': produtores, 'action': action})

    elif action == 'adicionar_produtor':
        if request.method == 'POST':
            form = ProdutorForm(request.POST)
            if form.is_valid():
                produto = form.save()
                Estoque.objects.create(produto=produto, quantidade=0, valor_total=0.0)
                messages.success(request, "Cadastro feito com sucesso!")
                return redirect(reverse('menu_gerente_action', kwargs={'action': 'listar_produtores'}))
        else:
            form = ProdutorForm()  # Formulário vazio para GET
        return render(request, 'produtos/menu_gerente.html', {'form': form, 'action': action})

    elif action == 'editar_produtor' and pk:
        produtor = get_object_or_404(Produtor, pk=pk)

        if request.method == 'POST':
            form = ProdutorForm(request.POST, instance=produtor)
            if form.is_valid():
                form.save()  # Salva as alterações
                messages.success(request, "Produtor atualizado com sucesso!")
                return redirect(reverse('menu_gerente_action', kwargs={'action': 'listar_produtores'}))
        else:
            form = ProdutorForm(instance=produtor)

        return render(request, 'produtos/menu_gerente.html', {'form': form, 'action': action})

    elif action == 'excluir_produtor' and pk:

        produtor = get_object_or_404(Produtor, pk=pk)

        if request.method == 'POST':

            produtor.delete()

            messages.success(request, "Produtor excluído com sucesso!")

            return redirect(reverse('menu_gerente_action', kwargs={'action': 'listar_produtores'}))

        return render(request, 'produtos/menu_gerente.html', {'produtor': produtor, 'action': action})

    elif action == 'listar_produtos':
        produtos = Produto.objects.all()
        return render(request, 'produtos/menu_gerente.html', {'produtos': produtos, 'action': action})

    elif action == 'adicionar_produto':
        if request.method == 'POST':
            form = ProdutoForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Produto adicionado com sucesso!")
                return redirect(reverse('menu_gerente_action', kwargs={'action': 'listar_produtos'}))
        else:
            form = ProdutoForm()
        return render(request, 'produtos/menu_gerente.html', {'form': form, 'action': action})

    elif action == 'editar_produto' and pk:
        produto = get_object_or_404(Produto, pk=pk)
        if request.method == 'POST':
            form = ProdutoForm(request.POST, instance=produto)
            if form.is_valid():
                form.save()
                messages.success(request, "Produto atualizado com sucesso!")
                return redirect(reverse('menu_gerente_action', kwargs={'action': 'listar_produtos'}))
        else:
            form = ProdutoForm(instance=produto)
        return render(request, 'produtos/menu_gerente.html', {'form': form, 'action': action, 'produto': produto})

    elif action == 'excluir_produto' and pk:
        produto = get_object_or_404(Produto, pk=pk)
        if request.method == 'POST':
            produto.delete()
            messages.success(request, "Produto excluído com sucesso!")
            return redirect(reverse('menu_gerente_action', kwargs={'action': 'listar_produtos'}))
        return render(request, 'produtos/menu_gerente.html', {'produto': produto, 'action': action})

    elif action == 'relatorio_estoque':
        relatorios = RelatorioEstoque.objects.all().order_by('-data_alteracao')  # Obter todos os relatórios, ordenados pela data
        return render(request, 'produtos/menu_gerente.html', {'relatorios': relatorios, 'action': action})


    return render(request, 'produtos/menu_gerente.html', {'action': 'inicio'})

from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProdutorPerfilForm
from django.contrib import messages
from .models import Produto, RelatorioEstoque

def menu_produtor(request, action=None, pk=None):
    if request.user.is_authenticated:
        if action == 'estoque':  # Para a página de estoque
            produtos = Produto.objects.all()  # Todos os produtos registrados no sistema

            if request.method == 'POST':  # Se o usuário estiver tentando adicionar ou vender estoque
                produto_id = request.POST.get('produto_id')
                quantidade = int(request.POST.get('quantidade'))
                produto = get_object_or_404(Produto, id=produto_id)

                # Adicionar estoque
                if 'adicionar' in request.POST:
                    produto.quantidade += quantidade
                    produto.save()

                    # Criar um relatório de estoque
                    relatorio = RelatorioEstoque(
                        produto=produto,
                        produtor=request.user,  # Usando o usuário logado (produtor)
                        quantidade_alterada=quantidade,
                        tipo_alteracao='adicao',  # Tipo da alteração
                    )
                    relatorio.save()  # Salva o relatório de alteração no estoque
                    messages.success(request, f"Estoque do produto {produto.nome} atualizado com sucesso!")

                elif 'vender' in request.POST:
                    if produto.quantidade >= quantidade:
                        produto.quantidade -= quantidade
                        produto.save()

                        # Criar um relatório de estoque
                        relatorio = RelatorioEstoque(
                            produto=produto,
                            produtor=request.user,  # Usando o usuário logado (produtor)
                            quantidade_alterada=quantidade,
                            tipo_alteracao='venda',  # Tipo da alteração
                        )
                        relatorio.save()  # Salva o relatório de alteração no estoque
                        messages.success(request, f"{quantidade} unidades de {produto.nome} foram vendidas.")
                    else:
                        messages.error(request, "Quantidade insuficiente no estoque.")

            return render(request, 'produtos/menu_produtor.html', {'produtos': produtos, 'action': action})

        elif action == 'perfil':
            # Aqui você deve buscar os dados do produtor logado, que já deve estar autenticado
            produtor = get_object_or_404(Produtor, usuario=request.user)

            if request.method == 'POST':
                form = ProdutorPerfilForm(request.POST, instance=produtor)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Seu perfil foi atualizado com sucesso!")
                    return redirect('menu_produtor_action', action='perfil')  # Redireciona para o perfil atualizado
            else:
                form = ProdutorPerfilForm(instance=produtor)

            return render(request, 'produtos/menu_produtor.html',
                          {'form': form, 'produtor': produtor, 'action': action})

        return render(request, 'produtos/menu_produtor.html',
                      {'action': 'inicio'})  # Redireciona para o início se não for encontrado nenhuma ação

    else:
        return redirect('login')  # Se o usuário não estiver autenticado, redireciona para login


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
    conteudo = ConteudoLogin.objects.filter(tipo_login='produtor').first()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            produtor = Produtor.objects.get(usuario=username)

            # Verifica se a senha fornecida corresponde à senha armazenada
            if check_password(password, produtor.senha):
                # Se a senha estiver correta, fazemos login
                request.session['produtor_id'] = produtor.id  # Armazenando o ID do produtor na sessão
                return redirect('menu_produtor')  # Redireciona para a tela do menu do produtor
            else:
                messages.error(request, 'Senha incorreta.')

        except Produtor.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')

    return render(request, 'produtos/login_produtor.html', {'conteudo': conteudo})

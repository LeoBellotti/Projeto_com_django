from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import Produto, PaginaInicial, ConteudoLogin, EstoqueChange, Pedido
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
                if 'entrada' in request.POST:
                    produto.quantidade += quantidade
                    produto.save()

                    # Criar um relatório de estoque
                    relatorio = RelatorioEstoque(
                        produto=produto,
                        produtor=request.user,  # Usando o usuário logado (produtor)
                        quantidade_alterada=quantidade,
                        tipo_alteracao='Entrada Registrada',  # Tipo da alteração
                    )
                    relatorio.save()  # Salva o relatório de alteração no estoque
                    messages.success(request, f"Estoque do produto {produto.nome} atualizado com sucesso!")

                elif 'remover' in request.POST:
                    if produto.quantidade >= quantidade:
                        produto.quantidade -= quantidade
                        produto.save()

                        # Criar um relatório de estoque
                        relatorio = RelatorioEstoque(
                            produto=produto,
                            produtor=request.user,  # Usando o usuário logado (produtor)
                            quantidade_alterada=quantidade,
                            tipo_alteracao='Remoção Registrada',  # Tipo da alteração
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

        elif action == 'gerar_pedidos':
            produtos = Produto.objects.all()  # Todos os produtos disponíveis
            cart = request.session.get('cart', {})  # Obtém o carrinho da sessão

            if request.method == 'POST':
                # Adicionar produto ao carrinho
                if 'adicionar' in request.POST:
                    produto_id = request.POST.get('produto_id')
                    quantidade = request.POST.get('quantidade')

                    if produto_id and quantidade:
                        produto = get_object_or_404(Produto, id=produto_id)
                        quantidade = int(quantidade)

                        if produto_id in cart:
                            cart[produto_id] += quantidade
                        else:
                            cart[produto_id] = quantidade

                        # Atualizar o carrinho na sessão
                        request.session['cart'] = cart
                        messages.success(request, f"{quantidade} unidades do produto {produto.nome} adicionadas ao carrinho.")
                    return redirect('menu_produtor_action', action='gerar_pedidos')

                # Remover produto do carrinho
                if 'remover' in request.POST:
                    produto_id = request.POST.get('produto_id')
                    if produto_id in cart:
                        del cart[produto_id]
                        request.session['cart'] = cart
                        messages.success(request, "Produto removido do carrinho.")
                    return redirect('menu_produtor_action', action='gerar_pedidos')

                # Gerar o pedido
                if 'gerar_pedido' in request.POST:
                    total_pedido = 0

                    for produto_id, quantidade in cart.items():
                        produto = Produto.objects.get(id=produto_id)
                        total = produto.preco * quantidade
                        total_pedido += total

                        # Criar o pedido no banco de dados
                        Pedido.objects.create(
                            produtor=request.user,
                            produto=produto,
                            quantidade=quantidade,
                            total=total
                        )

                        # Atualizar estoque
                        produto.quantidade -= quantidade
                        produto.save()

                        # Registrar a alteração no estoque
                        RelatorioEstoque.objects.create(
                            produto=produto,
                            quantidade_alterada=quantidade,
                            tipo_alteracao='Venda',
                            produtor=request.user
                        )

                    # Limpar o carrinho após o pedido
                    request.session['cart'] = {}
                    messages.success(request, f"Pedido gerado com sucesso! Valor total: R$ {total_pedido:.2f}")
                    return redirect('menu_produtor_action', action='gerar_pedidos')

            # Calcular o total do pedido
            cart_items = []
            total_pedido = 0
            for produto_id, quantidade in cart.items():
                produto = Produto.objects.get(id=produto_id)
                total = produto.preco * quantidade
                cart_items.append({
                    'produto': produto,
                    'quantidade': quantidade,
                    'total': total,
                })
                total_pedido += total

            return render(request, 'produtos/menu_produtor.html', {
                'produtos': produtos,
                'action': action,
                'cart_items': cart_items,
                'total_pedido': total_pedido,
            })

        return render(request, 'produtos/menu_produtor.html', {'action': 'inicio'})
    else:
        return redirect('login')

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

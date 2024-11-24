from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import Produto, PaginaInicial, ConteudoLogin, EstoqueChange, Pedido, LogSistema
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto
from .models import Produtor,Estoque
from .forms import ProdutoForm, ProdutorPerfilForm
from .forms import ProdutorForm
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProdutorPerfilForm
from django.contrib import messages
from .models import Produto, RelatorioEstoque
from django.contrib.auth import logout  # Importar logout do Django


@login_required(login_url='login_gerente')  # Especifica o redirecionamento para a página de login

def menu_gerente(request, action=None, pk=None):
    is_admin = request.user.is_staff  # Ou outro critério para identificar gerente
    produtor = None

    if not is_admin:
        try:
            produtor = Produtor.objects.get(usuario=request.user.username)
        except Produtor.DoesNotExist:
            messages.error(request, "Você não possui um perfil de produtor.")
            return redirect('login_produtor')

    if action == 'listar_produtores':
        produtores = Produtor.objects.all()  # Removido qualquer filtro desnecessário
        return render(request, 'produtos/menu_gerente.html', {'produtores': produtores, 'action': action})

    elif action == 'adicionar_produtor':
        if request.method == 'POST':
            form = ProdutorForm(request.POST)
            if form.is_valid():
                form.save()
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
                produto = form.save()  # Salva o produto
                Estoque.objects.create(produto=produto, quantidade=0,valor_total=0.0)  # Cria o estoque vinculado ao produto
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
        relatorios = RelatorioEstoque.objects.select_related('produtor', 'produto').order_by('-data')
        return render(request, 'produtos/menu_gerente.html', {

            'relatorios': relatorios,
            'action': action
        })

    elif action == 'estoque':
        produtos = Produto.objects.all()
        if request.method == 'POST':
            produto_id = request.POST.get('produto_id')
            quantidade = int(request.POST.get('quantidade'))
            produto = get_object_or_404(Produto, id=produto_id)

            # Entrada de estoque
            if 'entrada' in request.POST:
                produto.quantidade += quantidade
                produto.save()

                RelatorioEstoque.objects.create(
                    produto=produto,
                    quantidade_alterada=quantidade,
                    tipo_alteracao='Entrada Registrada',
                    produtor=produtor if produtor else None,  # Para produtores
                    admin=request.user if is_admin else None  # Para gerentes
                )
                messages.success(request, f"Entrada registrada: {quantidade} unidades de {produto.nome} adicionadas.")

            # Saída de estoque
            elif 'remover' in request.POST:
                if produto.quantidade >= quantidade:
                    produto.quantidade -= quantidade
                    produto.save()

                    RelatorioEstoque.objects.create(
                        produto=produto,
                        quantidade_alterada=quantidade,
                        tipo_alteracao='Saída Registrada',
                        produtor=produtor if produtor else None,  # Para produtores
                        admin=request.user if is_admin else None  # Para gerentes
                    )
                    messages.success(request, f"Saída registrada: {quantidade} unidades de {produto.nome} removidas.")
                else:
                    messages.error(request, "Quantidade insuficiente no estoque.")

        return render(request, 'produtos/menu_gerente.html', {'produtos': produtos, 'action': action})

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
                    return redirect('menu_gerente_action', action='gerar_pedidos')

                # Remover produto do carrinho
                if 'remover' in request.POST:
                    produto_id = request.POST.get('produto_id')
                    if produto_id in cart:
                        del cart[produto_id]
                        request.session['cart'] = cart
                        messages.success(request, "Produto removido do carrinho.")
                    return redirect('menu_gerente_action', action='gerar_pedidos')

                # Gerar o pedido
                if 'gerar_pedido' in request.POST:
                    total_pedido = 0

                    for produto_id, quantidade in cart.items():
                        produto = Produto.objects.get(id=produto_id)
                        total = produto.preco * quantidade
                        total_pedido += total

                        # Criar o pedido no banco de dados
                        Pedido.objects.create(
                            produtor=produtor if produtor else None,
                            admin=request.user if is_admin else None,
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
                            produtor=produtor if produtor else None,  # Para produtores
                            admin=request.user if is_admin else None  # Para gerentes
                        )

                    # Limpar o carrinho após o pedido
                    request.session['cart'] = {}
                    messages.success(request, f"Pedido gerado com sucesso! Valor total: R$ {total_pedido:.2f}")
                    return redirect('menu_gerente_action', action='gerar_pedidos')

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

            return render(request, 'produtos/menu_gerente.html', {
                'produtos': produtos,
                'action': action,
                'cart_items': cart_items,
                'total_pedido': total_pedido,
            })


    elif action == 'log_sistema':
        logs = LogSistema.objects.all().order_by('-data_entrada')
        return render(request, 'produtos/menu_gerente.html', {'logs': logs, 'action': action})

    return render(request, 'produtos/menu_gerente.html', {'action': 'inicio'})

def menu_produtor(request, action=None, pk=None):
    produtor_id = request.session.get('produtor_id')
    if not produtor_id:
        messages.error(request, "Você precisa fazer login para acessar esta página.")
        return redirect('login_produtor')

    try:
        # Busca o produtor pelo ID salvo na sessão
        produtor = Produtor.objects.get(id=produtor_id)
    except Produtor.DoesNotExist:
        messages.error(request, "Perfil de produtor não encontrado. Faça login novamente.")
        return redirect('login_produtor')
    if action == 'estoque':  # Página de Estoque
        produtos = Produto.objects.all()  # Lista de todos os produtos

        if request.method == 'POST':  # Adicionar ou remover do estoque
            produto_id = request.POST.get('produto_id')
            quantidade = int(request.POST.get('quantidade', 0))
            produto = get_object_or_404(Produto, id=produto_id)

            if 'entrada' in request.POST:  # Entrada de estoque
                produto.quantidade += quantidade
                produto.save()

                # Registro no relatório de estoque
                RelatorioEstoque.objects.create(
                    produto=produto,
                    produtor=produtor,  # Relacionando ao produtor logado
                    quantidade_alterada=quantidade,
                    tipo_alteracao='Entrada Registrada',
                )
                messages.success(request, f"Estoque do produto {produto.nome} atualizado com sucesso!")

            elif 'remover' in request.POST:  # Remoção de estoque
                if produto.quantidade >= quantidade:
                    produto.quantidade -= quantidade
                    produto.save()

                    # Registro no relatório de estoque
                    RelatorioEstoque.objects.create(
                        produto=produto,
                        produtor=produtor,
                        quantidade_alterada=quantidade,
                        tipo_alteracao='Remoção Registrada',
                    )
                    messages.success(request, f"{quantidade} unidades de {produto.nome} foram removidas do estoque.")
                else:
                    messages.error(request, "Quantidade insuficiente no estoque.")

        return render(request, 'produtos/menu_produtor.html', {'produtos': produtos, 'action': action})

    elif action == 'perfil':  # Página de Perfil
        form = ProdutorPerfilForm(instance=produtor)
        if request.method == 'POST':
            form = ProdutorPerfilForm(request.POST, instance=produtor)
            if form.is_valid():
                form.save()
                messages.success(request, "Perfil atualizado com sucesso!")
                return redirect('menu_produtor_action', action='perfil')

        return render(request, 'produtos/menu_produtor.html', {'form': form, 'produtor': produtor, 'action': action})

    elif action == 'gerar_pedidos':  # Página de Gerar Pedidos
        produtos = Produto.objects.all()
        cart = request.session.get('cart', {})  # Obtém o carrinho armazenado na sessão

        if request.method == 'POST':
            # Adicionar ao carrinho
            if 'adicionar' in request.POST:
                produto_id = request.POST.get('produto_id')
                quantidade = int(request.POST.get('quantidade', 0))

                if produto_id and quantidade > 0:
                    try:
                        produto = Produto.objects.get(id=produto_id)
                    except Produto.DoesNotExist:
                        messages.error(request, "Produto não encontrado. Tente novamente.")
                        return redirect('menu_produtor_action', action='gerar_pedidos')

                    if produto_id in cart:
                        cart[produto_id] += quantidade
                    else:
                        cart[produto_id] = quantidade

                    request.session['cart'] = cart
                    messages.success(request, f"{quantidade} unidades do produto {produto.nome} adicionadas ao carrinho.")
                else:
                    messages.error(request, "Informe um produto válido e uma quantidade maior que zero.")
                return redirect('menu_produtor_action', action='gerar_pedidos')

            # Remover do carrinho
            if 'remover' in request.POST:
                produto_id = request.POST.get('produto_id')
                if produto_id in cart:
                    del cart[produto_id]
                    request.session['cart'] = cart
                    messages.success(request, "Produto removido do carrinho.")
                return redirect('menu_produtor_action', action='gerar_pedidos')

            # Gerar pedido
            if 'gerar_pedido' in request.POST:
                total_pedido = 0

                for produto_id, quantidade in cart.items():
                    try:
                        produto = Produto.objects.get(id=produto_id)
                    except Produto.DoesNotExist:
                        messages.error(request, f"Produto com ID {produto_id} não encontrado. Pedido não foi gerado.")
                        continue

                    total = produto.preco * quantidade
                    total_pedido += total

                    # Criar o pedido no banco de dados
                    Pedido.objects.create(
                        produtor=produtor,
                        produto=produto,
                        quantidade=quantidade,
                        total=total,
                    )

                    # Atualizar estoque
                    produto.quantidade -= quantidade
                    produto.save()

                    # Registrar no relatório de estoque
                    RelatorioEstoque.objects.create(
                        produto=produto,
                        quantidade_alterada=quantidade,
                        tipo_alteracao='Venda',
                        produtor=produtor,
                    )

                request.session['cart'] = {}  # Limpa o carrinho
                messages.success(request, f"Pedido gerado com sucesso! Valor total: R$ {total_pedido:.2f}")
                return redirect('menu_produtor_action', action='gerar_pedidos')

        # Exibir o carrinho e total do pedido
        cart_items = []
        total_pedido = 0
        for produto_id, quantidade in cart.items():
            try:
                produto = Produto.objects.get(id=produto_id)
            except Produto.DoesNotExist:
                continue
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
        usuario = request.POST.get('username')
        senha = request.POST.get('password')
        try:
            produtor = Produtor.objects.get(usuario=usuario)
            if senha == produtor.senha:  # Valida a senha diretamente
                # Salvar o ID do produtor na sessão
                request.session['produtor_id'] = produtor.id
                messages.success(request, "Login realizado com sucesso!")

                # Registrar no log do sistema
                LogSistema.objects.create(
                    produtor=produtor,
                    acao="Login realizado"
                )

                return redirect('menu_produtor')  # Redireciona para o menu do produtor
            else:
                messages.error(request, "Senha incorreta. Tente novamente.")
        except Produtor.DoesNotExist:
            messages.error(request, "Usuário não encontrado. Verifique suas credenciais.")

    return render(request, 'produtos/login_produtor.html', {'conteudo': conteudo})



def logout_produtor(request):
    produtor_id = request.session.get('produtor_id')
    if produtor_id:
        try:
            produtor = Produtor.objects.get(id=produtor_id)

            # Registrar no log do sistema
            LogSistema.objects.create(
                produtor=produtor,
                acao="Logout realizado"
            )
        except Produtor.DoesNotExist:
            messages.error(request, "Erro ao registrar o logout.")

    # Limpar a sessão
    request.session.flush()

    messages.success(request, "Logout realizado com sucesso.")
    return redirect('login_produtor')

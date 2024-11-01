from django.urls import path
from .views import lista_produtos, adicionar_produto, editar_produto, deletar_produto, login_produtor, login_gerente, \
    listar_produtores, cadastrar_produtor, editar_produtor, deletar_produtor

urlpatterns = [
    path('login/gerente/', login_gerente, name='login_gerente'),  # Rota para o login do gerente
    path('produtores/', listar_produtores, name='listar_produtores'),
    path('produtores/cadastrar/', cadastrar_produtor, name='cadastrar_produtor'),
    path('produtores/editar/<int:pk>/', editar_produtor, name='editar_produtor'),
    path('produtores/deletar/<int:pk>/', deletar_produtor, name='deletar_produtor'),
    path('login/produtor/', login_produtor, name='login_produtor'),  # Rota para o login do produtor
    path('produtos/', lista_produtos, name='lista_produtos'),  # Rota para a lista de produtos
    path('produtos/adicionar/', adicionar_produto, name='adicionar_produto'),  # Rota para adicionar produto
    path('produtos/editar/<int:pk>/', editar_produto, name='editar_produto'),  # Rota para editar produto
    path('produtos/deletar/<int:pk>/', deletar_produto, name='deletar_produto'),  # Rota para deletar produto
]

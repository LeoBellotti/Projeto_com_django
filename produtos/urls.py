from django.urls import path
from . import views

urlpatterns = [
    # Login URLs
    path('login/gerente/', views.login_gerente, name='login_gerente'),
    path('login/produtor/', views.login_produtor, name='login_produtor'),

    # Menu Gerente URLs com ações e parâmetros opcionais para ações específicas
    path('menu/gerente/', views.menu_gerente, name='menu_gerente'),  # Menu padrão do gerente
    path('menu/gerente/<str:action>/', views.menu_gerente, name='menu_gerente_action'),  # Ações gerais
    path('menu/gerente/<str:action>/<int:pk>/', views.menu_gerente, name='menu_gerente_action_pk'),  # Ações com pk

    # Produto management URLs via ações
    path('menu/gerente/produtos/', views.menu_gerente, {'action': 'listar_produtos'}, name='listar_produtos'),
    path('menu/gerente/produtos/add/', views.menu_gerente, {'action': 'adicionar_produto'}, name='adicionar_produto'),
    path('menu/gerente/produtos/edit/<int:pk>/', views.menu_gerente, {'action': 'editar_produto'}, name='editar_produto'),
    path('menu/gerente/produtos/delete/<int:pk>/', views.menu_gerente, {'action': 'excluir_produto'}, name='excluir_produto'),

    # Produtor management URLs via ações
    path('menu/gerente/produtores/', views.menu_gerente, {'action': 'listar_produtores'}, name='listar_produtores'),

    path('menu/gerente/produtores/add/', views.menu_gerente, {'action': 'adicionar_produtor'}, name='adicionar_produtor'),

    path('menu/gerente/produtores/edit/<int:pk>/', views.menu_gerente, {'action': 'editar_produtor'}, name='editar_produtor'),
    path('menu/gerente/produtores/delete/<int:pk>/', views.menu_gerente, {'action': 'excluir_produtor'}, name='excluir_produtor'),

    # Menu Produtor URLs com ações e parâmetros opcionais para ações específicas
    path('menu/produtor/', views.menu_produtor, name='menu_produtor'),
    path('menu/produtor/<str:action>/', views.menu_produtor, name='menu_produtor_action'),
    path('menu/produtor/<str:action>/<int:pk>/', views.menu_produtor, name='menu_produtor_action_pk'),

    path('menu/produtor/', views.menu_produtor, {'action': 'estoque'}, name='listar_produtos'),
    path('menu/gerente/produtos/', views.menu_produtor, {'action': 'listar_produtos'}, name='listar_produtos_gerente'),
    path('menu/produtor/adicionar_estoque/', views.menu_produtor, {'action': 'adicionar_estoque'}, name='adicionar_estoque'),
    path('menu/produtor/venda_estoque/', views.menu_produtor, {'action': 'venda_estoque'}, name='venda_estoque'),

]

from django.urls import path
from . import views

urlpatterns = [
    path('login/gerente/', views.login_gerente, name='login_gerente'),
    path('menu/gerente/', views.menu_gerente, name='menu_gerente'),  # A URL principal do menu do gerente
    path('menu/gerente/<str:action>/', views.menu_gerente, name='menu_gerente_action'),  # URL para ações como "gerenciar"
    path('menu/gerente/<str:action>/<int:pk>/', views.menu_gerente, name='menu_gerente_action_pk'),  # Para editar ou excluir com ID
    path('login/produtor/', views.login_produtor, name='login_produtor'),
]

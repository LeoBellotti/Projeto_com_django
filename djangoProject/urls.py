from django.contrib import admin
from django.urls import path, include
from produtos.views import exibir_pagina_inicial  # Certifique-se de que está importando a função correta

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', exibir_pagina_inicial, name='pagina_inicial'),  # Atualize a referência aqui
    path('produtos/', include('produtos.urls')),  # Inclui as URLs do app produtos
]

from django.contrib import admin
from django.urls import path, include
from produtos.views import pagina_inicial  # Certifique-se de que está importando a função correta

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', pagina_inicial, name='pagina_inicial'),  # Define a página inicial diretamente na raiz
    path('produtos/', include('produtos.urls')),  # Inclui as URLs do app produtos
]

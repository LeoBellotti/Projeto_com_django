

from produtos.views import pagina_inicial  # Certifique-se de que está importando a função correta
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('pagina_inicial/', include('produtos.urls')),  # Use 'produtos' aqui
]







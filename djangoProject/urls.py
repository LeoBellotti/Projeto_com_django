from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from produtos.views import exibir_pagina_inicial  # Certifique-se de importar a função correta

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', exibir_pagina_inicial, name='pagina_inicial'),  # Define a página inicial diretamente na raiz
    path('produtos/', include('produtos.urls')),  # Inclui as URLs do app produtos
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

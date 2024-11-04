from django.contrib import admin
from .models import Produto
from .models import PaginaInicial
from .models import ConteudoLogin

admin.site.register(ConteudoLogin)

admin.site.register(PaginaInicial)
admin.site.register(Produto)

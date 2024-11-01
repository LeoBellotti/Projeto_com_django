from django.contrib import admin
from .models import Produto
from .models import PaginaInicial

admin.site.register(PaginaInicial)
admin.site.register(Produto)

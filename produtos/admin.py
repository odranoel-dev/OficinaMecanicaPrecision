from django.contrib import admin
from .models import Produto

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'quantidade') # Colunas visíveis
    list_filter = ('preco',) # Filtro por preço
    search_fields = ('nome',) # Pesquisa por nome

admin.site.register(Produto, ProdutoAdmin)

from django.contrib import admin
from .models import Produto

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('peca', 'quantidade', 'prateleira', 'codigo', 'minimo')  # campos existentes
    list_filter = ('quantidade', 'minimo')  # filtros que fazem sentido
    search_fields = ('peca',)  # pesquisa por campo existente

admin.site.register(Produto, ProdutoAdmin)

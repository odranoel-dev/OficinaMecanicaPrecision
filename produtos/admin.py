from django.contrib import admin
# Importe os novos modelos Cliente e Venda, além do Produto
from .models import Produto, Cliente, Venda

# Configuração do Admin para Produto (você já tinha)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('peca', 'quantidade', 'prateleira', 'codigo', 'minimo')
    list_filter = ('quantidade', 'minimo')
    search_fields = ('peca',)

# --- INÍCIO DO NOVO CÓDIGO ---

# Configuração do Admin para Cliente
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone')
    search_fields = ('nome', 'email', 'telefone')

# Configuração do Admin para Venda
class VendaAdmin(admin.ModelAdmin):
    list_display = ('data_venda', 'cliente', 'produto', 'quantidade')
    list_filter = ('data_venda', 'produto', 'cliente')
    search_fields = ('produto__peca', 'cliente__nome')
    # Deixa a data como "read-only" pois é definida automaticamente
    readonly_fields = ('data_venda',)

# --- FIM DO NOVO CÓDIGO ---

# Registros no site de administração
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Cliente, ClienteAdmin) # Novo registro
admin.site.register(Venda, VendaAdmin)     # Novo registro
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'), 
    path('movimentacao/', views.movimentacao_estoque, name='movimentacao_estoque'),  
]

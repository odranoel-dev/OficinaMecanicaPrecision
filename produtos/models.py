from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100, default="Desconhecido")
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField()
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome

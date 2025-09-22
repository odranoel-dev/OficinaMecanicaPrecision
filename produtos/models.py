from django.db import models

class Produto(models.Model):
    peca = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    prateleira = models.CharField(max_length=100)
    codigo = models.IntegerField()
    minimo = models.IntegerField()

    def __str__(self):
        return self.peca

class Movimentacao(models.Model):
    TIPO_MOVIMENTACAO = [
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMENTACAO)
    quantidade = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True)
    observacao = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.tipo == 'ENTRADA':
            self.produto.quantidade += self.quantidade
        elif self.tipo == 'SAIDA':
            self.produto.quantidade -= self.quantidade
        self.produto.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo} - {self.produto.peca} ({self.quantidade})"

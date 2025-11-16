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

class Cliente(models.Model):
    """
    Modelo para armazenar dados básicos do cliente.
    """
    nome = models.CharField(max_length=200, help_text="Nome completo do cliente")
    email = models.EmailField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nome

class Venda(models.Model):
    """
    Modelo para registrar uma venda simples.
    """
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        help_text="Selecione um cliente (opcional)"
    )
    produto = models.ForeignKey(
        'Produto',  # Assume que o modelo Produto está no mesmo app
        on_delete=models.PROTECT, 
        help_text="Selecione a peça vendida"
    )
    quantidade = models.PositiveIntegerField(
        help_text="Quantidade vendida"
    )
    data_venda = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data da Venda"
    )

    def __str__(self):
        return f"Venda de {self.quantidade}x {self.produto.peca} em {self.data_venda.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
        ordering = ['-data_venda']
from django import forms
from .models import Venda, Produto, Cliente, Movimentacao

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['produto', 'tipo', 'quantidade', 'observacao']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class VendaForm(forms.ModelForm):
    
    class Meta:
        model = Venda
        fields = ['cliente', 'produto', 'quantidade']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select form-control'}),
            'produto': forms.Select(attrs={'class': 'form-select form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Qtd.'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona um "placeholder" amigável aos campos
        self.fields['cliente'].empty_label = "Selecione um Cliente (Opcional)"
        self.fields['produto'].empty_label = "Selecione a Peça"

        # Garante que um cliente "Consumidor Final" exista para vendas rápidas
        if not Cliente.objects.filter(nome="Consumidor Final").exists():
             Cliente.objects.create(nome="Consumidor Final", email="consumidor@final.com")
        
        # Opcional: Definir "Consumidor Final" como padrão
        try:
            consumidor_final = Cliente.objects.get(nome="Consumidor Final")
            self.fields['cliente'].initial = consumidor_final.pk
        except Cliente.DoesNotExist:
            pass # Ignora se não encontrar

    def clean(self):
        """
        Validação customizada para o formulário.
        Verifica se a quantidade em estoque é suficiente.
        """
        cleaned_data = super().clean()
        produto = cleaned_data.get('produto')
        quantidade_vendida = cleaned_data.get('quantidade')

        if produto and quantidade_vendida:
            if quantidade_vendida <= 0:
                raise forms.ValidationError({
                    'quantidade': "A quantidade deve ser pelo menos 1."
                })

            if quantidade_vendida > produto.quantidade:
                # Gera um erro de validação que será exibido no template
                raise forms.ValidationError(
                    f"Estoque insuficiente para '{produto.peca}'. "
                    f"Você tentou vender {quantidade_vendida}, mas há apenas {produto.quantidade} em estoque."
                )
        
        return cleaned_data
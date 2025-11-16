from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Produto, Movimentacao, Venda, Cliente
from .forms import MovimentacaoForm, VendaForm
from django.db import transaction

def lista_produtos(request):
    produtos = Produto.objects.all().order_by('peca')
    return render(request, 'produtos/lista.html', {'produtos': produtos})

def movimentacao_estoque(request):
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movimentacao_estoque')  # redireciona para a mesma página
    else:
        form = MovimentacaoForm()

    movimentacoes = Movimentacao.objects.all().order_by('-data')
    return render(request, 'produtos/movimentacao.html', {
        'form': form,
        'movimentacoes': movimentacoes
    })

def registrar_venda(request):
    """
    View para registrar uma nova venda e atualizar o estoque.
    """
    if request.method == 'POST':
        form = VendaForm(request.POST)
        
        if form.is_valid():
            try:
                # transaction.atomic garante que ambas as operações (salvar venda e
                # atualizar estoque) sejam concluídas com sucesso, ou nenhuma delas.
                with transaction.atomic():
                    # Pega os dados validados do formulário
                    produto = form.cleaned_data.get('produto')
                    quantidade_vendida = form.cleaned_data.get('quantidade')

                    # 1. Salva a venda (sem salvar no DB ainda)
                    venda = form.save(commit=False)
                    
                    # 2. Atualiza o estoque do produto
                    # A validação de estoque suficiente já foi feita no form.clean()
                    produto.quantidade -= quantidade_vendida
                    produto.save()
                    
                    # 3. Agora salva o registro da Venda no banco de dados
                    venda.save()
                    
                    messages.success(request, 
                        f"Venda de {quantidade_vendida}x {produto.peca} registrada! "
                        f"Estoque atualizado para {produto.quantidade}."
                    )
                    # Redireciona para a lista de produtos (assumindo que o nome da URL é 'lista_produtos')
                    return redirect('lista_produtos') 

            except Exception as e:
                # Em caso de um erro inesperado, exibe uma mensagem
                messages.error(request, f"Ocorreu um erro inesperado: {e}")

        else:
            # Se o formulário não for válido (ex: estoque insuficiente),
            # o template será renderizado novamente e o form.non_field_errors
            # (no template) mostrará a mensagem de erro do forms.py.
            messages.warning(request, "Não foi possível registrar a venda. Por favor, corrija os erros abaixo.")

    else: # Se for um request GET
        form = VendaForm()

    # Para exibir vendas recentes na mesma página
    vendas_recentes = Venda.objects.all().order_by('-data_venda')[:10]

    context = {
        'form': form,
        'vendas_recentes': vendas_recentes
    }
    # Renderiza o novo template
    return render(request, 'produtos/vendas/venda_form.html', context)

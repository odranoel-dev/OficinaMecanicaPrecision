from django.shortcuts import render, redirect
from .models import Produto, Movimentacao
from .forms import MovimentacaoForm

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

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.contrib import messages
from .models import TiposExame, PedidosExame, SolicitacaoExame
import datetime

@login_required(login_url='/usuarios/logar')
def solicitar_exames(request):
    tipos_exames = TiposExame.objects.all()
    data = datetime.datetime.now()

    if request.POST:
        exames_ids = request.POST.getlist('exames')
        solicitacao_exames = TiposExame.objects.filter(id__in=exames_ids) 
        preco_total = sum(exame.preco for exame in solicitacao_exames if exame.disponivel)

        context = {
            'tipos_exames': tipos_exames,
            'solicitacao_exames': solicitacao_exames,
            'preco_total': preco_total,
            'data': data,
        }
        return render(request, 'solicitar_exames.html', context)   
    return render(request, 'solicitar_exames.html', {'tipos_exames': tipos_exames, 'data': data})


@login_required(login_url='/usuarios/logar')
def fechar_pedido(request):
    if request.POST:
        exames_id = request.POST.getlist('exames')
        tipos_exames = TiposExame.objects.filter(id__in=exames_id)
        pedidos_exame = PedidosExame.objects.create(usuario=request.user)
        solicitacao_exames_temp = [
            SolicitacaoExame(usuario=request.user, tipo_exame=tipo_exame, status='E')
            for tipo_exame in tipos_exames
        ]
        SolicitacaoExame.objects.bulk_create(solicitacao_exames_temp)
        pedidos_exame.solicitacao_exames.set(solicitacao_exames_temp)
        messages.add_message(request, constants.SUCCESS, 'Pedido de exame realizado com sucesso!')
        return redirect('/exames/gerenciar_pedidos/')
    return redirect('solicitar_exames')


@login_required(login_url='/usuarios/logar')
def gerenciar_pedidos(request):
    pedidos_exames = PedidosExame.objects.filter(usuario=request.user)
    return render(request, 'gerenciar_pedidos.html', {'pedidos_exames': pedidos_exames})


@login_required(login_url='/usuarios/logar')
def cancelar_pedido(request, pedido_id):
    pedido = PedidosExame.objects.get(id=pedido_id)
    if not  request.user == pedido.usuario:
        messages.add_message(request, constants.ERROR, 'Usuário não tem permissão para cancelar o pedido!')
        return redirect('/exames/gerenciar_pedidos/')
    pedido.agendado = False
    pedido.save()
    messages.add_message(request, constants.SUCCESS, 'Pedido de exame cancelado com sucesso!')
    return redirect('/exames/gerenciar_pedidos/')


@login_required(login_url='/usuarios/logar')
def gerenciar_exames(request):
    exames = SolicitacaoExame.objects.filter(usuario=request.user)
    return render(request, 'gerenciar_exames.html', {'exames':exames})


@login_required(login_url='/usuarios/logar')
def permitir_abrir_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
    if not exame.requer_senha:
        try:
            return redirect(exame.resultado.url)
        except:
            messages.add_message(request, constants.ERROR, 'PDF do exame não foi cadastrado!')
            return redirect('exames:gerenciar_exames')
    return redirect(f'/exames/solicitar_senha_exame/{exame_id}')


@login_required(login_url='/usuarios/logar')
def solicitar_senha_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
    if request.method == 'GET':
        return render(request, 'solicitar_senha_exames.html', {'exame': exame})
    elif request.method == 'POST':
        senha = request.POST.get('senha')
        if senha == exame.senha:
          try:
            return redirect(exame.resultado.url)
          except:
            messages.add_message(request, constants.ERROR, 'PDF do exame não foi cadastrado!')
            return redirect('exames:gerenciar_exames')
        else:
            messages.add_message(request, constants.ERROR, 'Senha inválida.')
            return redirect('exames:solicitar_senha_exame', exame_id=exame.id)
        
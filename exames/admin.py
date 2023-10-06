from django.contrib import admin
from . import models


@admin.register(models.TiposExame)
class TiposExamesAdmin(admin.ModelAdmin):
    list_display = ('nome','tipo', 'preco', 'disponivel', 'horario_inicial')

@admin.register(models.SolicitacaoExame)
class SolicitacaoExameAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_exame', 'status', 'resultado', 'requer_senha', 'senha')

@admin.register(models.PedidosExame)
class PedidosExamesAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'agendado', 'data')

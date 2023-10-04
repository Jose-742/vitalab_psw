from django.db import models
from django.contrib.auth.models import User

TIPO_CHOICES = (
    ('I', 'Exame de imagem'),
    ('S', 'Exame de sangue'),
)

STATUS_CHOICES = (
    ('E', 'Em análise'),
    ('F', 'Finalizado')
)
class TiposExame(models.Model):
    nome = models.CharField(max_length=50)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    preco = models.FloatField()
    disponivel = models.BooleanField(default=True)
    horario_inicial = models.IntegerField()
    horario_final = models.IntegerField()

    def __str__(self):
        return self.nome

class SolicitacaoExame(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exame = models.ForeignKey(TiposExame, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    resultado = models.FileField(upload_to="resultados", null=True, blank=True)
    requer_senha = models.BooleanField(default=False)
    senha = models.CharField(max_length=6, null=True, blank=True)
  
    def __str__(self):
        return f'{self.usuario} | {self.exame.nome}'

class PedidosExame(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exames = models.ManyToManyField(SolicitacaoExame)
    agendado = models.BooleanField(default=True)
    data = models.DateField()
    
    def __str__(self):
        return f'{self.usuario} | {self.data}'
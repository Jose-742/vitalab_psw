from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.conf import settings
from secrets import token_urlsafe
from datetime import timedelta
import datetime

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
    tipo_exame = models.ForeignKey(TiposExame, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    resultado = models.FileField(upload_to="resultados", null=True, blank=True)
    requer_senha = models.BooleanField(default=False)
    senha = models.CharField(max_length=6, null=True, blank=True)
  
    def badge_template(self):
        if self.status == "E":
            classes = 'bg-warning text-dark'
            text = 'Em análise'
        elif self.status == "F":
            classes = 'bg-success'
            text = 'Finalizado'
        
        return mark_safe(f'<span class="badge {classes}">{text}</span>')
        

    def __str__(self):
        return f'{self.usuario} | {self.tipo_exame.nome}'

class PedidosExame(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    solicitacao_exames = models.ManyToManyField(SolicitacaoExame)
    agendado = models.BooleanField(default=True)
    data = models.DateField(default=datetime.datetime.now)
    
    def __str__(self):
        return f'{self.usuario} | {self.data}'

class AcessoMedico(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    identificacao = models.CharField(max_length=50)
    tempo_de_acesso = models.IntegerField() # Em horas
    criado_em = models.DateTimeField(default=datetime.datetime.now)
    data_exames_iniciais = models.DateField()
    data_exames_finais = models.DateField()
    token = models.CharField(max_length=20, null=True, blank=True)

    @property 
    def status(self):
        return 'Expirado' if timezone.now() > (self.criado_em + timedelta(hours=self.tempo_de_acesso)) else 'Ativo'
        
    @property
    def url(self):
        return f'{settings.URL_LINKS}exames/acesso_medico/{self.token}'

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = token_urlsafe(6)

        super(AcessoMedico, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.token
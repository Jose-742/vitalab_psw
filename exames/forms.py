from django import forms 
from . import models

class AcessoMedicoForm(forms.ModelForm):
    class Meta:
        model=models.AcessoMedico
        fields = ('identificacao', 'tempo_de_acesso', 'data_exames_iniciais', 'data_exames_finais',)


'''
   
    identificacao = models.CharField(max_length=50)
    tempo_de_acesso = models.IntegerField() # Em horas
    data_exames_iniciais = models.DateField()
    data_exames_finais = models.DateField()
'''
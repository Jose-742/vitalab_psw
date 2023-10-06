# Generated by Django 4.2.5 on 2023-10-05 01:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exames', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pedidosexame',
            old_name='exames',
            new_name='solicitacao_exames',
        ),
        migrations.RenameField(
            model_name='solicitacaoexame',
            old_name='exame',
            new_name='tipo_exame',
        ),
        migrations.AlterField(
            model_name='pedidosexame',
            name='data',
            field=models.DateField(default=datetime.datetime(2023, 10, 4, 22, 56, 41, 620688)),
        ),
    ]

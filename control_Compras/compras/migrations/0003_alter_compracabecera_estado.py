# Generated by Django 4.1.7 on 2023-09-11 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0002_compracabecera_usuario_aprobado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compracabecera',
            name='estado',
            field=models.CharField(choices=[('0', 'Pendiente'), ('1', 'Registrado'), ('2', 'Aprobado Encargado'), ('3', 'Autorizado Gerencia'), ('4', 'Entregado'), ('5', 'Cerrado')], default='0', max_length=1),
        ),
    ]

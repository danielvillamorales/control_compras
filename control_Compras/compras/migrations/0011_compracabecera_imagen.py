# Generated by Django 4.1.7 on 2023-09-18 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0010_compracabecera_valor_real'),
    ]

    operations = [
        migrations.AddField(
            model_name='compracabecera',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='compras'),
        ),
    ]
